from typing import Any

import numpy as np
import numpy.typing as npt
from scipy.stats import entropy  # type:ignore

from .catalog import ALCatalog
from .selectioncriterion import AbstractSelectionCriterion


class MostCertainSampling(AbstractSelectionCriterion):
    """Selects the training examples most far away from the
    decision threshold at 0.50 / 50 % class probability.
    """

    name = ALCatalog.QueryType.MOST_CERTAIN

    def __call__(self, prob_mat: npt.NDArray[Any]) -> npt.NDArray[Any]:
        min_prob: npt.NDArray[Any] = np.amin(np.abs(prob_vec - 0.5), axis=1)  # type: ignore
        return min_prob


class MinEntropy(AbstractSelectionCriterion):
    """Selects the training examples with the lowest entropy
    at the probability level. This method is usable for
    Multilabel Classification.
    """

    name = ALCatalog.QueryType.MIN_ENTROPY

    def __call__(self, prob_mat: npt.NDArray[Any]) -> npt.NDArray[Any]:
        min_entropy: npt.NDArray[Any] = -entropy(prob_mat, axis=1)  # type: ignore
        return min_entropy


class MostConfidence(AbstractSelectionCriterion):
    """Selects the training examples with the highest probability
    for **any** label in the probability matrix.
    """

    name = ALCatalog.QueryType.MOST_CONFIDENCE

    def __call__(self, prob_mat: npt.NDArray[Any]) -> npt.NDArray[Any]:
        confidence: npt.NDArray[Any] = np.amax(prob_mat, axis=1)  # type: ignore
        return confidence


class LabelMaximizer(AbstractSelectionCriterion):
    """Identity function. This is usable for finding the
    instance with the highest probability when the matrix is
    sliced for one label only.

    TODO: Make the label a parameter
    """

    name = ALCatalog.QueryType.LABELMAXIMIZER

    def __call__(self, prob_mat: npt.NDArray[Any]) -> npt.NDArray[Any]:
        return prob_mat


class LabelMaximizerNew(AbstractSelectionCriterion):
    name = ALCatalog.QueryType.LABELMAXIMIZER_NEW

    def __init__(self, label_column: int):
        super().__init__()
        self.label_column = label_column

    def __call__(self, prob_mat: npt.NDArray[Any]) -> npt.NDArray[Any]:
        prob_mat_sliced = prob_mat[:, self.label_column]
        return prob_mat_sliced
