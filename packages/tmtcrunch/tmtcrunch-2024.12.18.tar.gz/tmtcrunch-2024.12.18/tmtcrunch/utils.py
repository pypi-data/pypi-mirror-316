"""Miscellaneous functions."""

__all__ = [
    "protein_abundance",
    "drop_decoys_from_protein_group",
    "get_gene_name",
    "groupwise_qvalues",
    "indicator",
    "weighted_mean",
    "mean_and_std",
    "uniq",
]


import re
from collections.abc import Iterable
from typing import Callable, Union

import numpy as np

try:
    from astropy.stats import biweight_scale, median_absolute_deviation
except ModuleNotFoundError:
    from .astropy_stats import biweight_scale, median_absolute_deviation

import pandas as pd
from pyteomics import auxiliary as paux

from .altsp import GeneralPsmGroup


def uniq(x: Iterable[str], sort=True) -> list:
    """
    Filter out repeated elements from the input list.

    :param x: Iterable.
    :param sort: If True, return sorted list.
    :return: List of unique elements.
    """
    y = list(set(x))
    y = sorted(y) if sort else y
    return y


def get_gene_name(protein_descr: str, missing_gene: str = "_void_") -> str:
    """
    Parse protein description for gene name.

    :param protein_descr: Protein description from FASTA header.
    :param missing_gene: String to return if gene is not found, defaults to '_void_'.
    :return: Gene name.
    """
    res = re.search(r"GN=(\S*)", protein_descr)
    if res:
        return res.group(1)
    return missing_gene


def drop_decoys_from_protein_group(
    data: pd.DataFrame, decoy_prefix: str = "DECOY_"
) -> pd.DataFrame:
    """
    Drop decoy proteins from protein group and sort remaining proteins within their
    group.

    :param data: DataFrame with 'protein' and 'protein_descr' columns.
    :param decoy_prefix: Decoy prefix, defaults to 'DECOY_'.
    :return: DataFrame of the same format as input data.
    """
    df_tmp = data[["protein", "protein_descr"]]
    df_tmp = df_tmp.assign(
        p_d=lambda df: [dict(zip(p, d)) for p, d in zip(df.protein, df.protein_descr)]
    )
    df_tmp.p_d = df_tmp.p_d.apply(
        lambda x: {p: d for p, d in sorted(x.items()) if not p.startswith(decoy_prefix)}
    )
    df_tmp = df_tmp.assign(
        protein=lambda df: [list(q.keys()) for q in df.p_d],
        protein_descr=lambda df: [list(q.values()) for q in df.p_d],
    )
    data.protein = df_tmp.protein
    data.protein_descr = df_tmp.protein_descr
    return data


def groupwise_qvalues(df_psm: pd.DataFrame, psm_group: GeneralPsmGroup) -> pd.DataFrame:
    """
    Calculate groupwise qvalues for `psm_group` in `df_psm`. Return new DataFrame with
    group PSMs and q-values stored in `group_q` column.

    :param df_psm: Scavager PSMs_full DataFrame.
    :param psm_group: PSMs group to calculate qvalues.
    :return: DataFrame with group PSMs.
    """

    group_ind = psm_group.target_ind | psm_group.decoy_ind
    df_group = df_psm[group_ind]

    group_pep_ratio = df_group["decoy2"].sum() / df_group["decoy"].sum()
    # filter out decoy1, which were used for CatBoost training
    df_group = df_group[~df_group["decoy1"]].copy()

    res = paux.qvalues(
        df_group,
        key="ML score",
        is_decoy="decoy2",
        remove_decoy=False,
        ratio=group_pep_ratio,
        formula=1,
        full_output=True,
        correction=1,
    )
    df_group["group_q"] = res["q"]
    return df_group


def indicator(
    df: pd.DataFrame, cols: list[str], ind_func: Callable[[float], bool] = bool
) -> pd.Series:
    """
    Return boolean array for indexing rows where `ind_func` is True for all columns in
    the DataFrame.

    :param df: DataFrame.
    :param cols: List of columns.
    :param ind_func: Boolean function.
    :return: Boolean array.
    """
    return df[cols].map(ind_func).all(axis="columns")


def weighted_mean(
    data: np.array,
    data_err: np.array = None,
    axis: int = 0,
    c: float = 6.0,
    mean0=None,
) -> Union[float, np.array]:
    """
    Calculate the weighted mean along the specified axis.

    If `data_err` is not None, it is added to the weights and then biweight location
    is computed. Otherwise, the weighted mean is equivalent to the biweight_location.
    Based on biweight location:
    https://docs.astropy.org/en/stable/api/astropy.stats.biweight.biweight_location.html

    :param data: Input data.
    :param data_err: Data uncertainty, optional.
    :param axis: Axis along which a mean is calculated.
    :param c: Tuning constant for the biweight estimator.
    :param mean0: Initial guess for mean.
    :return: Weighted mean of the input data.
    """
    if mean0 is None:
        mean0 = np.median(data, axis=axis)

    mad = median_absolute_deviation(data, axis=axis)

    d = data - mean0
    weight = d**2
    if data_err is not None:
        weight += data_err**2

    if np.isscalar(mean0) and (mad == 0.0 or np.isnan(mad)):
        correction = 0
    else:
        with np.errstate(divide="ignore", invalid="ignore"):
            u = weight / (c * mad) ** 2
            mask = u >= 1
            u = (1 - u) ** 2
            u[mask] = 0
            correction = np.sum(u * d, axis=axis) / np.sum(u, axis=axis)

    if np.isscalar(mean0):
        # if data_err is big, sum(u) could be 0 and correction is undefined
        correction = 0 if np.isnan(correction) else correction
        wmean = mean0 + correction
    else:
        correction = np.where(np.isnan(correction), 0, correction)
        wmean = mean0 + np.where(mad == 0, 0, correction)

    return wmean


def mean_and_std(
    data: np.array, data_err: np.array, axis: int = 0
) -> tuple[np.array, np.array]:
    """
    Robust estimation for the mean and std based on Tukey's biweight.

    :param data: Input data.
    :param data_err: Data uncertainty, optional.
    :param axis: Axis along which statistic is calculated.
    :return: Tuple of mean and standard deviation.
    """
    wmean0 = weighted_mean(data, data_err, axis=axis)
    wmean = weighted_mean(data, data_err, axis=axis, mean0=wmean0)
    std = biweight_scale(data, axis=axis, M=wmean)
    return wmean, std


def protein_abundance(
    df_psm: pd.DataFrame,
    groupby_cols: list,
    specimen_cols: list,
    error_cols: list = None,
) -> pd.DataFrame:
    """
    Calculate protein abundance and its standard deviation.

    The protein abundance is computed as a weighted mean of reduced intensities of PSMs.
    Standard deviation of abundance is computed by biweight_scale.

    :param df_psm: DataFrame with reduced intensities and optionally errors.
    :param groupby_cols: df_psm columns to group PSMs for a protein.
    :param specimen_cols: List of specimen columns.
    :param error_cols: List of error columns corresponding to the specimen columns,
        optional.
    :return: DataFrame of protein abundance and its std error.
    """
    multi_index = pd.MultiIndex.from_tuples(
        df_psm.groupby(groupby_cols).indices.keys(),
        names=groupby_cols,
    )
    std_cols = [f"{col}_std" for col in specimen_cols]
    df_protein = pd.DataFrame(
        index=multi_index,
        columns=specimen_cols + std_cols,
        dtype=float,
    )
    for mi, df in df_psm.groupby(groupby_cols):
        data = np.array(df[specimen_cols])
        data_err = None if error_cols is None else np.array(df[error_cols])
        df_protein.loc[mi] = np.hstack(mean_and_std(data, data_err))
    return df_protein.reset_index()
