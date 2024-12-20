from __future__ import annotations

import collections
import itertools
import logging
import math
import os
import random
from abc import ABC, abstractmethod
from typing import (
    Any,
    Callable,
    Deque,
    Dict,
    FrozenSet,
    Generic,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

from instancelib.typehints import DT, KT, LT, RT, VT

from ..activelearning.ensembles import ManualEnsemble
from ..activelearning.ml_based import MLBased
from ..environment.base import IT, AbstractEnvironment
from ..machinelearning import AbstractClassifier
from ..utils import get_random_generator
from .base import ActiveLearner

_T = TypeVar("_T")

LOGGER = logging.getLogger(__name__)


def intersection(first: FrozenSet[_T], *others: FrozenSet[_T]) -> FrozenSet[_T]:
    return first.intersection(*others)


def powerset(iterable: Iterable[_T]) -> FrozenSet[FrozenSet[_T]]:
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    result = itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )
    return frozenset(map(frozenset, result))  # type: ignore


class Estimator(
    ManualEnsemble[IT, KT, DT, VT, RT, LT], Generic[IT, KT, DT, VT, RT, LT]
):
    def __init__(
        self,
        env: AbstractEnvironment[IT, KT, DT, VT, RT, LT],
        learners: Sequence[
            ActiveLearner[IT, KT, DT, VT, RT, LT],
        ],
        probabilities: Optional[Sequence[float]] = None,
        rng: Any = None,
        *_,
        identifier: Optional[str] = None,
        **__,
    ) -> None:
        probs = (
            [1.0 / len(learners)] * len(learners)
            if probabilities is None
            else probabilities
        )
        super().__init__(env, learners, probs, rng, *_, identifier=identifier, **__)

    @classmethod
    def builder(
        cls,
        learner_builders: Sequence[
            Callable[..., ActiveLearner[IT, KT, DT, VT, RT, LT]]
        ],
        probabilities: Optional[Sequence[float]] = None,
        *_: Any,
        **__: Any,
    ) -> Callable[..., ManualEnsemble[IT, KT, DT, VT, RT, LT]]:
        probs = (
            [1.0 / len(learner_builders)] * len(learner_builders)
            if probabilities is None
            else probabilities
        )
        return super().builder(learner_builders, probs, *_, **__)


class RetryEstimator(
    Estimator[IT, KT, DT, VT, RT, LT], Generic[IT, KT, DT, VT, RT, LT]
):
    def __next__(self) -> IT:
        # Choose the next random learners
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
            ins = next(learner)

        # Set the instances as sampled by learner with key al_idx and return the instance
        self._sample_dict[ins.identifier] = self.learners.index(learner)
        return ins


class CycleEstimator(
    Estimator[IT, KT, DT, VT, RT, LT], Generic[IT, KT, DT, VT, RT, LT]
):
    def __init__(
        self,
        env: AbstractEnvironment[IT, KT, DT, VT, RT, LT],
        learners: Sequence[ActiveLearner[IT, KT, DT, VT, RT, LT]],
        probabilities: Optional[Sequence[float]] = None,
        rng: Any = None,
        *_,
        identifier: Optional[str] = None,
        **__,
    ) -> None:
        super().__init__(
            env, learners, probabilities, rng, *_, identifier=identifier, **__
        )
        self.learnercycle = itertools.cycle(self.learners)

    def _choose_learner(self) -> ActiveLearner[IT, KT, DT, VT, RT, LT]:
        return next(self.learnercycle)
