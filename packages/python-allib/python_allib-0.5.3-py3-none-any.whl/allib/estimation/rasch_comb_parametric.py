from dataclasses import dataclass
from logging import currentframe
from os import spawnlp
from typing import Any, Generic, List, Optional, Sequence, Tuple

import multiprocessing as mp
import itertools
import functools
import warnings
import instancelib
from numpy.linalg import LinAlgError
from numba.experimental import jitclass
from numba import jit, types, typed, int32, prange # type: ignore
from numba.typed import List as NumbaList

import pandas as pd

from ..activelearning.estimator import Estimator
import numpy as np
import numpy.typing as npt
from .rasch import EMRaschCombined

from ..typehints.typevars import KT, DT, VT, RT, LT

spec = [
    ("positive", int32[:]),
    ("estimate", int32[:]),
    ("negative", int32[:]),
    ("observed", int32[:]),
    ("positive_estimate", int32[:]),
    ("negative_estimate", int32[:]),
    ("positive_observed", int32[:]),
    ("negative_observed", int32[:]),
]

@jitclass(spec)
class Masks:
    def __init__(self, 
                 positive: npt.NDArray[Any], 
                 estimate: npt.NDArray[Any], 
                 negative: npt.NDArray[Any], 
                 observed: npt.NDArray[Any], 
                 positive_estimate: npt.NDArray[Any], 
                 negative_estimate: npt.NDArray[Any], 
                 positive_observed: npt.NDArray[Any], 
                 negative_observed: npt.NDArray[Any]):
        self.positive = positive
        self.estimate = estimate
        self.negative = negative
        self.observed = observed
        self.positive_estimate = positive_estimate
        self.negative_estimate = negative_estimate
        self.positive_observed = positive_observed
        self.negative_observed = negative_observed

def create_mask(poses: List[bool], estes: List[bool]) -> Masks:
    def convert(bool_list: Sequence[bool]) -> npt.NDArray[Any]:
        converted = np.array([i for (i,b) in enumerate(bool_list) if b], dtype=np.int32)
        return converted
    positive = convert(poses)
    estimate = convert(estes)
    neges = [not(m) for m in poses]
    obses = [not(m) for m in estes]
    negative = convert(neges)
    observed = convert(obses)
    positive_estimate = convert(NumbaList([est & pos for est, pos in zip(estes, poses)]))
    negative_estimate = convert(NumbaList([est & neg for est, neg in zip(estes, neges)]))
    positive_observed = convert(NumbaList([obs & pos for obs, pos in zip(obses, poses)]))
    negative_observed = convert(NumbaList([obs & neg for obs, neg in zip(obses, neges)]))
    return Masks(positive, estimate, 
                 negative, observed, 
                 positive_estimate, negative_estimate, 
                 positive_observed, negative_observed)
@jit(nopython=True) # type: ignore
def l2(b0: npt.NDArray[Any],
       design_mat: npt.NDArray[Any],
       counts: npt.NDArray[Any],
       lam: float = 0.0,
       tolerance: float = 1e-8,
       max_it: int = 10000,
       epsilon: float = 0.1
       ) -> npt.NDArray[Any]:
    counts = counts + epsilon
    current_tolerance = 1
    b = b0
    it = 0
    while current_tolerance > tolerance and it < max_it:
        it = it + 1

        mu = np.exp(design_mat @ b0)
        all_but_first_b0: npt.NDArray[Any] = b0[1:]
        lbpart: npt.NDArray[Any] = 2 * np.concatenate(
            (
                np.array([0.0]),
                (lam * all_but_first_b0)
        ))
        design_mat_t = design_mat.conj().transpose()
        db = design_mat_t @ counts - design_mat_t @ mu - lbpart
        repeat_count = b0.shape[0] - 1
        other_lb_part = np.hstack((np.array([0.0]), np.repeat(lam, repeat_count)))
        I = (design_mat_t @ np.diag(mu)) @ design_mat + \
            2 * np.diag(other_lb_part)
        try:
            invI = np.linalg.inv(I)
        except Exception: # LinAlgException
            # Change lambda if the matrix is not invertible
            lam = 1e-6 if lam == 0 else 10 * lam
        else:
            # If inversion succeeded, calculate new coefficients b
            b = b0 + invI @ db
            current_tolerance = np.sum(np.abs(b0 - b))
            b0 = b
    # if it >= max_it:
    #     warnings.warn(
    #         f"Exceeded maximum L2 iterations ({max_it}). Estimate might not be accurate")
    return b


@jit(nopython=True)  # type: ignore
def calc_deviance(y: npt.NDArray[Any], y_hat: npt.NDArray[Any]) -> float:
    pos_y_idx = np.where(y > 0)
    pos_y = y[pos_y_idx]
    deviance = (
        2 * np.sum(pos_y * np.log(pos_y / y_hat[pos_y_idx])) -
        2 * np.sum(y - y_hat))
    return deviance


def add_missing_count_rows(freq_df: pd.DataFrame, n_pos: float, n_neg: float) -> pd.DataFrame:
    pos_dict = {
        **{col: 0 for col in freq_df.columns},
        **{"count": n_pos, "positive": 1}
    }
    neg_dict = {
        **{col: 0 for col in freq_df.columns},
        **{"count": n_neg, "positive": 0}
    }
    new_freq_df = (
        freq_df
        .append(pos_dict, ignore_index=True)
        .append(neg_dict, ignore_index=True)
    )
    return new_freq_df


def l2_format(freq_df: pd.DataFrame, learner_cols: Sequence[str]) -> pd.DataFrame:
    order_cols = ["positive", *learner_cols]
    df = freq_df.sort_values(order_cols)
    df.insert(0, "intercept", 1)
    return df

@jit(nopython=True)  # type: ignore
def parameter_ci(estimate: float, se: float) -> Tuple[float, float]:
    var_min = estimate - 2 * se
    var_max = estimate + 2 * se
    return var_max, var_min

@jit(nopython=True)  # type: ignore
def calculate_estimate(intercept: float, pos: float) -> float:
    return np.exp(intercept + pos)

def calculate_ci_rasch(intercept: float,
                       positive: float,
                       intercept_se: float,
                       positive_se: float) -> Tuple[float, float]:
    intercepts = parameter_ci(intercept, intercept_se)
    positive_par = parameter_ci(positive, positive_se)
    combinations = itertools.product(intercepts, positive_par)
    results = list(itertools.starmap(calculate_estimate, combinations))
    min_result = min(results)
    max_result = max(results)
    return min_result, max_result

@jit(nopython=True)  # type: ignore
def initial_fit(n_not_read: float, design_mat: npt.NDArray[Any]) -> npt.NDArray[Any]:
    not_read = np.array([n_not_read])
    b0 = np.hstack(
        (
            np.log(not_read),
            np.repeat(0.0, design_mat.shape[1] - 1)
    ))
    return b0

@jit(nopython=True)  # type: ignore
def rasch_glm(design_mat: npt.NDArray[Any],
              efit: npt.NDArray[Any],
              counts: npt.NDArray[Any],
              b0: npt.NDArray[Any],
              masks: Masks
              ) -> Tuple[npt.NDArray[Any], npt.NDArray[Any], float]:
    obs_counts = counts[masks.observed]
    beta = l2(b0, design_mat, counts)
    mfit = np.exp(design_mat @ beta)
    obs_fitted = mfit[masks.observed]
    deviance = calc_deviance(obs_counts, obs_fitted)
    return beta, mfit, deviance





@jit(nopython=True)  # type: ignore
def rasch_em(design_mat: npt.NDArray[Any], 
             counts: npt.NDArray[Any],
             n_dataset: float,
             masks: Masks,
             proportion: float,
             tolerance: float = 1e-5,
             max_it=1000) -> Tuple[npt.NDArray[Any], npt.NDArray[Any], float]:
    orig_counts = counts[masks.observed]
    n_not_read = n_dataset - np.sum(orig_counts)
    
    n_pos = proportion * n_not_read
    n_neg = (1 - proportion) * n_not_read
    efit = counts

    efit[masks.positive_estimate] = n_pos
    efit[masks.negative_estimate] = n_neg

    b0 = initial_fit(n_not_read, design_mat)
    beta, mfit, deviance = rasch_glm(design_mat, efit, counts, b0, masks)
    current_tolerance = 1
    # Expectation Maximization
    it = 0
    while current_tolerance > tolerance:
        old_deviance = deviance
        efit[masks.estimate] = mfit[masks.estimate] * n_not_read / np.sum(mfit[masks.estimate])
        beta, mfit, deviance = rasch_glm(design_mat, efit, counts, beta, masks)
        current_tolerance = old_deviance - deviance
        if it > max_it:
            #warnings.warn(
            #    f"Exceeded maximum EM iterations ({max_it}). Estimate might not be accurate")
            return beta, mfit, deviance
    return beta, mfit, deviance

@jit(nopython=True, parallel=True) # type: ignore
def rasch_numpy(design_mat: npt.NDArray[Any],
                counts: npt.NDArray[Any],
                n_dataset: float,
                masks: Masks,
                proportions: npt.NDArray[Any] = np.array([0.001, 0.01, 0.1, 0.5, 0.75, 0.9]),
                tolerance: float = 1e-5,
                max_it=1000
                ) -> Tuple[npt.NDArray[Any], npt.NDArray[Any], float]:
    deviances = np.zeros(proportions.shape)
    betas = np.zeros((proportions.shape[0], design_mat.shape[1]))
    mfits = np.zeros((proportions.shape[0], design_mat.shape[0]))
    num_proportions = proportions.shape[0]
    n_not_read = n_dataset - np.sum(counts[masks.observed])
    for idx in prange(num_proportions):
        proportion = proportions[idx]
        b0 = initial_fit(n_not_read, design_mat)
        beta, mfit, deviance = rasch_em(design_mat, counts, n_dataset, masks, proportion, tolerance, max_it)
        betas[idx,:] = beta
        mfits[idx,:] = mfit
        deviances[idx] = deviance
    best_beta = np.zeros((design_mat.shape[1],))
    best_mfit = np.zeros((design_mat.shape[0],))
    best_deviance = 2000000.0
    for idx in range(num_proportions):
        current_beta = betas[idx,:]
        current_mfit = mfits[idx,:]
        current_deviance = deviances[idx]
        if current_deviance < best_deviance:
            best_deviance = current_deviance
            best_beta = current_beta
            best_mfit = current_mfit
    return best_beta, best_mfit, best_deviance

@jit(nopython=True) # type: ignore
def rasch_numpy_single_thread(design_mat: npt.NDArray[Any],
                counts: npt.NDArray[Any],
                n_dataset: float,
                masks: Masks,
                proportions: npt.NDArray[Any] = np.array([0.001, 0.01, 0.1, 0.5, 0.75, 0.9]),
                tolerance: float = 1e-5,
                max_it=1000
                ) -> Tuple[npt.NDArray[Any], npt.NDArray[Any], float]:
    deviances = np.zeros(proportions.shape)
    betas = np.zeros((proportions.shape[0], design_mat.shape[1]))
    mfits = np.zeros((proportions.shape[0], design_mat.shape[0]))
    num_proportions = proportions.shape[0]
    for idx in range(num_proportions):
        proportion = proportions[idx]
        beta, mfit, deviance = rasch_em(design_mat, counts, n_dataset, masks, proportion, tolerance, max_it)
        betas[idx,:] = beta
        mfits[idx,:] = mfit
        deviances[idx] = deviance
    best_beta = np.zeros((design_mat.shape[1],))
    best_mfit = np.zeros((design_mat.shape[0],))
    best_deviance = 2000000.0
    for idx in range(num_proportions):
        current_beta = betas[idx,:]
        current_mfit = mfits[idx,:]
        current_deviance = deviances[idx]
        if current_deviance < best_deviance:
            best_deviance = current_deviance
            best_beta = current_beta
            best_mfit = current_mfit
    return best_beta, best_mfit, best_deviance


def rasch_estimate_parametric(freq_df: pd.DataFrame,
                   n_dataset: int,
                   tolerance: float = 1e-5,
                   max_it: int = 2000,
                   multinomial_size: int = 50) -> Tuple[float, float, float]:
    # Calculate general frequency statistics
    counts: npt.NDArray[Any] = freq_df["count"].values  # type: ignore
    # Add place holder rows for the counts that we aim to estimate
    df_w_missing = add_missing_count_rows(freq_df, float("nan"), float("nan"))

    # Change the dataframe in the correct format for the L2 algorithm
    learner_cols = list(df_w_missing
                        .filter(regex=r"^(?:(?!positive$).)+$")
                        .filter(regex=r"^learner")
                        )
    df_formatted = l2_format(df_w_missing, learner_cols)

    # Calculate row masks to select data from the matrices and vectors
    est_mask: List[bool] = list(df_formatted[learner_cols].sum(axis=1) <= 0)
    pos_mask: List[bool] = list(df_formatted.positive > 0)
    masks = create_mask(pos_mask, est_mask)
    
    design_mat: npt.NDArray[Any] = (
        df_formatted.loc[:, df_formatted.columns != 'count']  # type: ignore
        .values)  # type: ignore

    counts: npt.NDArray[Any] = df_formatted["count"].values  # type: ignore

    beta, mfit, deviance = rasch_numpy(
        design_mat, counts, n_dataset, masks, tolerance=tolerance, max_it=max_it)
    positive_estimate: float = mfit[masks.positive_estimate][0]
    p_vals = mfit / np.sum(mfit)
    multinomial_fits: npt.NDArray[Any] = np.random.multinomial(
        n_dataset, p_vals, multinomial_size)
    low_estimate = positive_estimate
    high_estimate = positive_estimate
    if positive_estimate <= 2:
        workload = [
            (design_mat, np.array(sample), n_dataset, masks) 
            for sample in multinomial_fits.tolist()]
        with mp.Pool(7) as pool:
            results = pool.starmap(rasch_numpy, workload)
        estimates: List[float] = [fitted[masks.positive_estimate][0]
                                for (_, fitted, _) in results]
        low_estimate = np.percentile(estimates, 2.5)
        high_estimate = np.percentile(estimates, 97.5)
    return positive_estimate, low_estimate, high_estimate

@jit(nopython=True, parallel=True) # type: ignore
def rasch_parallel(design_mat: npt.NDArray[Any], 
                   rounded_mfits: npt.NDArray[Any], 
                   n_dataset: int, masks: Masks):
    deviances = np.zeros(rounded_mfits.shape[0])
    betas = np.zeros((rounded_mfits.shape[0], design_mat.shape[1]))
    mfits = np.zeros((rounded_mfits.shape[0], design_mat.shape[0]))
    num_mfits = rounded_mfits.shape[0]
    for idx in prange(num_mfits):
        mfit_sample = rounded_mfits[idx,:]
        beta, mfit, deviance = rasch_numpy_single_thread(design_mat, mfit_sample, n_dataset, masks) 
        betas[idx,:] = beta
        mfits[idx,:] = mfit
        deviances[idx] = deviance
    results = NumbaList()
    for idx in range(num_mfits):
        result = (betas[idx,:], mfits[idx,:], deviances[idx])
        results.append(result)
    return results
        
def rasch_estimate_parametric_approx(freq_df: pd.DataFrame,
                   n_dataset: int,
                   tolerance: float = 1e-5,
                   max_it: int = 2000,
                   multinomial_size: int = 50) -> Tuple[float, float, float]:
    # Calculate general frequency statistics
    counts: npt.NDArray[Any] = freq_df["count"].values  # type: ignore
    # Add place holder rows for the counts that we aim to estimate
    df_w_missing = add_missing_count_rows(freq_df, float("nan"), float("nan"))

    # Change the dataframe in the correct format for the L2 algorithm
    learner_cols = list(df_w_missing
                        .filter(regex=r"^(?:(?!positive$).)+$")
                        .filter(regex=r"^learner")
                        )
    df_formatted = l2_format(df_w_missing, learner_cols)

    # Calculate row masks to select data from the matrices and vectors
    est_mask: List[bool] = list(df_formatted[learner_cols].sum(axis=1) <= 0)
    pos_mask: List[bool] = list(df_formatted.positive > 0)
    masks = create_mask(pos_mask, est_mask)
    
    design_mat: npt.NDArray[Any] = (
        df_formatted.loc[:, df_formatted.columns != 'count']  # type: ignore
        .values)  # type: ignore

    counts: npt.NDArray[Any] = df_formatted["count"].values  # type: ignore

       
    beta, mfit, deviance = rasch_numpy(
        design_mat, counts, n_dataset, masks, tolerance=tolerance, max_it=max_it)
    positive_estimate: float = mfit[masks.positive_estimate][0]
    
    # Calculate standard error on predictors
    mat_w = np.diag(mfit)
    design_mat_t = design_mat.conj().transpose()
    vcov = np.linalg.inv(design_mat_t @ mat_w @ design_mat)
    
    predictors_sampled: npt.NDArray[Any] = np.random.multivariate_normal(beta, vcov, size=50)
    sampled_mfits = np.exp(design_mat @ predictors_sampled.T).T
    rounded_mfits = np.round(sampled_mfits)
    low_estimate = positive_estimate
    high_estimate = positive_estimate
    obs_pos = np.sum(counts[masks.positive_observed])
    if True:
        results = rasch_parallel(design_mat, rounded_mfits, n_dataset, masks)
        estimates: List[float] = [fitted[masks.positive_estimate][0]
                                for (_, fitted, _) in results]
        low_estimate = np.percentile(estimates, 2.5)
        high_estimate = np.percentile(estimates, 97.5)
    return positive_estimate, low_estimate, high_estimate




class EMRaschRidgeParametricPython(
        EMRaschCombined[KT, DT, VT, RT, LT],
        Generic[KT, DT, VT, RT, LT]):
    def __init__(self):
        super().__init__()
        self.df: Optional[pd.DataFrame] = None
        self.est = float("nan")
        self.est_low = float("nan")
        self.est_high = float("nan")

    def _start_r(self) -> None:
        pass

    def calculate_estimate(self,
                           estimator: Estimator[Any, KT, DT, VT, RT, LT],
                           label: LT) -> Tuple[float, float, float]:
        pos_count = estimator.env.labels.document_count(label)
        dataset_size = len(estimator.env.dataset)
        df = self.get_occasion_history(estimator, label)
        if self.df is None or not self.df.equals(df):
            self.df = df
            self.est, self.est_low, self.est_up = rasch_estimate_parametric_approx(
                df, dataset_size)
        horizon = self.est + pos_count
        horizon_low = self.est_low + pos_count
        horizon_up = self.est_up + pos_count
        return horizon, horizon_low, horizon_up