from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Optional,
    Sequence,
    Set,
    TypeVar,
)
from typing_extensions import Self

import instancelib as il
import numpy as np  # type: ignore
from instancelib import Instance
from instancelib.typehints.typevars import LMT, PMT

from ..activelearning.insclass import ILMLBased
from ..environment.base import AbstractEnvironment
from ..machinelearning import AbstractClassifier
from ..utils import get_random_generator
from .base import ActiveLearner
from .ml_based import MLBased
from .poolbased import PoolBasedAL

from ..typehints.typevars import IT, KT, DT, VT, RT, LT, LVT, PVT

LOGGER = logging.getLogger(__name__)


class AbstractEnsemble(ABC, Generic[IT, KT, DT, VT, RT, LT]):
    _name = "AbstractEnsemble"
    learners: Sequence[ActiveLearner[IT, KT, DT, VT, RT, LT]]
    env: AbstractEnvironment[IT, KT, DT, VT, RT, LT]
    _has_ordering: bool

    @abstractmethod
    def _choose_learner(self) -> ActiveLearner[IT, KT, DT, VT, RT, LT]:
        """Internal functions that selects the next active learner for the next query

        Returns:
            ActiveLearner[IT, KT, DT, VT, RT, LT]: One of the learners from the ensemble
        """
        raise NotImplementedError

    @property
    def has_ordering(self) -> bool:
        return self._has_ordering

    def update_ordering(self):
        """Updates the ordering for all learners of the ensemble"""
        for learner in self.learners:
            learner.update_ordering()
        self._has_ordering = True
        return True

    def __next__(self) -> IT:
        learner = self._choose_learner()
        return next(learner)

    @ActiveLearner.label_log
    def set_as_labeled(self, instance: Instance[KT, DT, VT, RT]) -> None:
        self.env.unlabeled.discard(instance)
        self.env.labeled.add(instance)

    def set_as_unlabeled(self, instance: Instance[KT, DT, VT, RT]) -> None:
        """Mark the instance as unlabeled

        Parameters
        ----------
        instance : Instance
            The now labeled instance
        """
        self.env.labeled.discard(instance)
        self.env.unlabeled.add(instance)


class ManualEnsemble(
    AbstractEnsemble[IT, KT, DT, VT, RT, LT],
    PoolBasedAL[IT, KT, DT, VT, RT, LT],
    Generic[IT, KT, DT, VT, RT, LT],
):
    _name = "Ensemble"

    def __init__(
        self,
        env: AbstractEnvironment[IT, KT, DT, VT, RT, LT],
        learners: Sequence[ActiveLearner[IT, KT, DT, VT, RT, LT],],
        probabilities: Sequence[float],
        rng: Any = None,
        *_,
        identifier: Optional[str] = None,
        **__,
    ) -> None:
        super().__init__(env, identifier=identifier)
        self.learners = learners
        self.probabilities = probabilities
        self._sample_dict: Dict[KT, int] = {}
        self._rng: Any = get_random_generator(rng)

    def _choose_learner(self) -> ActiveLearner[IT, KT, DT, VT, RT, LT]:
        """Internal functions that selects the next active learner for the next query

        Returns
        -------
        ActiveLearner[IT, KT, DT, VT, RT, LT]
            One of the learners from the ensemble
        """
        idxs = np.arange(len(self.learners))
        al_idx: int = self._rng.choice(idxs, size=1, p=self.probabilities)[0]
        learner = self.learners[al_idx]
        return learner

    def __next__(self) -> IT:
        # Select the learner
        learner = self._choose_learner()

        # Select the next instance from the learner
        ins = next(learner)

        # Check if the instance identifier has not been labeled already
        while ins.identifier in self.env.labeled:
            # This instance has already been labeled my another learner.
            # Skip it and mark as labeled
            learner.set_as_labeled(ins)
            LOGGER.info(
                "The document with key %s was already labeled. Skipping", ins.identifier
            )
            learner = self._choose_learner()
            ins = next(learner)

        # Set the instances as sampled by learner with key al_idx and return the instance
        self._sample_dict[ins.identifier] = self.learners.index(learner)
        return ins

    def set_as_labeled(self, instance: Instance[KT, DT, VT, RT]) -> None:
        self.env.labeled.add(instance)
        self.env.unlabeled.discard(instance)
        if instance.identifier in self._sample_dict:
            learner = self.learners[self._sample_dict[instance.identifier]]
            learner.set_as_labeled(instance)

    def set_as_unlabeled(self, instance: Instance[KT, DT, VT, RT]) -> None:
        self.env.unlabeled.add(instance)
        self.env.labeled.discard(instance)
        if instance.identifier in self._sample_dict:
            learner = self.learners[self._sample_dict[instance.identifier]]
            learner.set_as_unlabeled(instance)
            del self._sample_dict[instance.identifier]

    @classmethod
    def builder(
        cls,
        learner_builders: Sequence[
            Callable[..., ActiveLearner[IT, KT, DT, VT, RT, LT]]
        ],
        probabilities: Sequence[float],
        *_: Any,
        **__: Any,
    ) -> Callable[..., Self]:
        def wrap_func(
            env: AbstractEnvironment[IT, KT, DT, VT, RT, LT], *args, **kwargs
        ):
            learners = [
                builder(env.from_environment(env), *args, **kwargs)
                for builder in learner_builders
            ]
            return cls(env, learners, probabilities)

        return wrap_func


class StrategyEnsemble(
    AbstractEnsemble[IT, KT, DT, VT, RT, LT],
    MLBased[IT, KT, DT, VT, RT, LT, LVT, PVT],
    Generic[IT, KT, DT, VT, RT, LT, LVT, PVT],
):
    _name = "StrategyEnsemble"

    def __init__(
        self,
        env: AbstractEnvironment[IT, KT, DT, VT, RT, LT],
        classifier: AbstractClassifier[KT, VT, LT, LVT, PVT],
        learners: Sequence[ActiveLearner[IT, KT, DT, VT, RT, LT],],
        fallback: ActiveLearner[IT, KT, DT, VT, RT, LT],
        probabilities: Sequence[float],
        rng: Any = None,
        *_,
        identifier: Optional[str] = None,
        **__,
    ) -> None:
        super().__init__(env, classifier, fallback)
        self.learners = learners
        self.probabilities = probabilities
        self._rng: Any = get_random_generator(rng)
        self.sampled: Set[KT] = set()
        self._has_ordering: bool = False

    def update_ordering(self) -> bool:
        successful = super().update_ordering()
        if successful:
            self.sampled = set()
        return successful

    def _choose_learner(self) -> ActiveLearner[IT, KT, DT, VT, RT, LT]:
        """Internal functions that selects the next active learner for the next query

        Returns:
            ActiveLearner[IT, KT, DT, VT, RT, LT]: One of the learners from the ensemble
        """
        idxs = np.arange(len(self.learners))
        al_idx: int = self._rng.choice(idxs, size=1, p=self.probabilities)[0]
        learner = self.learners[al_idx]
        return learner

    def __next__(self) -> IT:
        result = super().__next__()
        while result.identifier in self.sampled:
            result = super().__next__()
        self.sampled.add(result.identifier)
        return result


class ILStrategyEnsemble(
    AbstractEnsemble[IT, KT, DT, VT, RT, LT],
    ILMLBased[IT, KT, DT, VT, RT, LT, LMT, PMT],
    Generic[IT, KT, DT, VT, RT, LT, LMT, PMT],
):
    def __init__(
        self,
        env: AbstractEnvironment[IT, KT, DT, VT, RT, LT],
        classifier: il.AbstractClassifier[IT, KT, DT, VT, RT, LT, LMT, PMT],
        learners: Sequence[ActiveLearner[IT, KT, DT, VT, RT, LT],],
        fallback: ActiveLearner[IT, KT, DT, VT, RT, LT],
        probabilities: Sequence[float],
        rng: Any = None,
        *_,
        identifier: Optional[str] = None,
        **__,
    ) -> None:
        super().__init__(env, classifier, fallback, identifier=identifier)
        self.learners = learners
        self.probabilities = probabilities
        self._rng = get_random_generator(rng)
        self.sampled: Set[KT] = set()
        self._has_ordering: bool = False

    def update_ordering(self) -> bool:
        successful = super().update_ordering()
        if successful:
            self.sampled = set()
        return successful

    def _choose_learner(self) -> ActiveLearner[IT, KT, DT, VT, RT, LT]:
        """Choose an Active Learning from the options according to
        the given probabilities

        Returns
        -------
        ActiveLearner[IT, KT, DT, VT, RT, LT]
            The chosen ActiveLearner
        """
        idxs = np.arange(len(self.learners))
        al_idx: int = self._rng.choice(idxs, size=1, p=self.probabilities)[0]
        learner = self.learners[al_idx]
        return learner

    def __next__(self) -> IT:
        result = super().__next__()
        while result.identifier in self.sampled:
            result = super().__next__()
        self.sampled.add(result.identifier)
        return result
