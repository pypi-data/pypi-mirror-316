"""TMTCrunch main module."""

__all__ = [
    "cli_main",
    "process_single_batch",
    "process_single_file",
]

import logging
import os.path
import sys
from argparse import ArgumentParser
from ast import literal_eval

import numpy as np
import pandas as pd

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from . import __version__
from .altsp import PrimeGroupsCollection, PsmGroup, generate_prefix_collection
from .config import DEFAULT_CONFIG, format_settings, update_settings
from .utils import (
    drop_decoys_from_protein_group,
    get_gene_name,
    groupwise_qvalues,
    indicator,
    protein_abundance,
    uniq,
)

logger = logging.getLogger(__name__)


def process_single_file(file: str, settings: dict) -> pd.DataFrame:
    """
    Perform qroupwise analysis of PSMs from single fraction.

    :param file: Path to Scavager *_PSMs_full.tsv file.
    :param settings: TMTCrunch settings.
    :return: DataFrame with filtered PSMs.
    """
    decoy_prefix = settings["decoy_prefix"]
    logger.info(f"Processing {file}")
    df_psm = pd.read_table(
        file, converters={key: literal_eval for key in ["protein", "protein_descr"]}
    )
    if settings["groupwise"]:
        prefix_collection = generate_prefix_collection(settings["target_prefixes"])
        primes = PrimeGroupsCollection(prefix_collection, df_psm)

        logger.info(f"Prime PSM groups:\n{primes}\n")
        dframes = {
            group_name: pd.DataFrame() for group_name in settings["psm_group"].keys()
        }
        for group_name, group_cfg in settings["psm_group"].items():
            group_fdr = group_cfg["fdr"]
            group_psm = PsmGroup(
                group_cfg["descr"],
                target_prefixes=group_cfg["prefixes"],
                prime_groups_collection=primes,
            )
            logger.info(f"{group_psm}\n")
            df_psm_group = groupwise_qvalues(df_psm, group_psm)
            fdr_steps = 5
            passed = [
                df_psm_group[df_psm_group["group_q"] < fdr].shape[0]
                for fdr in np.linspace(group_fdr / fdr_steps, group_fdr, fdr_steps)
            ]
            logger.info(f"PSMs at fdr=[{group_fdr / fdr_steps}, {group_fdr}]: {passed}")
            df_psm_group = df_psm_group[df_psm_group["group_q"] < group_fdr]
            df_psm_group = df_psm_group[~df_psm_group["decoy"]]
            group_psm_passed = PsmGroup(
                f"PSMs passed at fdr={group_fdr}",
                target_prefixes=group_cfg["prefixes"],
                prime_groups_collection=PrimeGroupsCollection(
                    prefix_collection, df_psm_group
                ),
            )
            logger.info(
                f"PSMs passed at fdr={group_fdr}: {df_psm_group.shape[0]}\n"
                f"{group_psm_passed.format(False)}\n"
            )
            df_psm_group["psm_group"] = group_name
            dframes[group_name] = df_psm_group
        df_psm = pd.concat(dframes.values(), ignore_index=True)
    else:
        # TODO: drop unused column
        df_psm["psm_group"] = ""
    df_psm = drop_decoys_from_protein_group(df_psm, decoy_prefix)
    # TODO: sort genes within group in accordance with the orger of proteins
    df_psm["gene"] = df_psm.protein_descr.apply(
        lambda x: uniq([get_gene_name(d) for d in x])
    )
    df_psm["protein_str"] = df_psm.protein.apply(", ".join)
    df_psm["gene_str"] = df_psm.gene.apply(", ".join)
    df_psm["file"] = f"{file}"
    cols = [
        "psm_group",
        "peptide",
        "gene",
        "gene_str",
        "protein",
        "protein_str",
        "protein_descr",
        "file",
    ]
    cols += settings["keep_columns"]
    cols += settings["gis_columns"] + settings["specimen_columns"]
    return df_psm[cols]


def process_single_batch(
    files: list[str], settings: dict
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Prepare batch for merging with other batches.

    Normalize tmt channel to account for loading difference. Reduce channel intensities
    with respect to GIS, calculate protein abundance from individual PSMs, and group
    result by PSM groups, genes, and proteins.

    :param files: Scavager *_PSMs_full.tsv files.
    :param settings: TMTCrunch settings.
    :return: tuple of DataFrames for PSMs, proteins, and genes.
    """
    logger.info(f"Total files in the batch: {len(files)}")
    df_psm = pd.concat(
        [process_single_file(file, settings) for file in files], ignore_index=True
    )
    gis_cols = settings["gis_columns"]
    spn_cols = settings["specimen_columns"]
    tmt_cols = settings["gis_columns"] + settings["specimen_columns"]

    # TODO: Drop PSMs olny with failed GIS channels.
    # protein_abundance() has to be resistant to the missing values.
    # ind_gis_non_zero = indicator(df_psm, cols=gis_cols, ind_func=bool)
    ind_all_non_zero = indicator(df_psm, cols=tmt_cols, ind_func=bool)
    ind_all_finite = indicator(df_psm, cols=spn_cols, ind_func=np.isfinite)

    n_total = df_psm.shape[0]
    df_psm = df_psm[ind_all_non_zero & ind_all_finite]
    n_bad = n_total - df_psm.shape[0]
    n_peptides = len(uniq(df_psm["peptide"].to_list(), sort=False))
    total_message = (
        f"Total PSMs:                     {n_total:>7}\n"
        f"PSMs with failed channels:      {n_bad:>7}\n"
    )

    # Normalize intensity per channel to account for loading difference.
    # If MS/MS were reproducible, sum() could be used for normalization.
    df_psm.loc[:, tmt_cols] /= np.mean(df_psm[tmt_cols], axis=0)
    # Switch to natural logarithm for further analysis.
    # The absolute error for log(x) is the relative error for x
    # due to d(log(x)) = dx/x and we like it.
    df_psm.loc[:, tmt_cols] = np.log(df_psm[tmt_cols])

    df_psm["gis_mean"] = np.mean(df_psm[gis_cols], axis=1)
    df_psm["gis_err"] = np.std(df_psm[gis_cols], axis=1)
    # Reduce individual intensities with respect to the mean GIS intensity.
    df_psm[tmt_cols] -= np.array(df_psm["gis_mean"])[:, np.newaxis]

    # Assemble df_protein and df_gene from df_psm.
    # psm_group, gene name, and protein name are used for multi-indexing
    # in df_protein and df_gene.
    df_psm_short = df_psm[["psm_group", "gene_str", "protein_str"] + spn_cols].copy()
    df_psm_short.rename(
        columns={"gene_str": "gene", "protein_str": "protein"}, inplace=True
    )

    if len(gis_cols) >= 2:
        spn_err_cols = [f"{col}_err" for col in spn_cols]
        df_psm_short[spn_err_cols] = (
            np.ones(df_psm[spn_cols].shape) * np.array(df_psm["gis_err"])[:, np.newaxis]
        )
    else:
        # gis_err is undefined for data with one GIS channel.
        spn_err_cols = None

    df_protein = protein_abundance(
        df_psm_short,
        ["psm_group", "gene", "protein"],
        spn_cols,
        spn_err_cols,
    )
    df_gene = protein_abundance(
        df_psm_short,
        ["psm_group", "gene"],
        spn_cols,
        spn_err_cols,
    )

    total_message += (
        f"Total PSMs used for assembling: {df_psm.shape[0]:>7}\n"
        f"Total peptides:                 {n_peptides:>7}\n"
        f"Total protein groups:           {df_protein.shape[0]:>7}\n"
        f"Total genes groups:             {df_gene.shape[0]:>7}\n"
    )
    logger.info("Summary:\n" + total_message)
    return df_psm, df_protein, df_gene


def cli_main() -> None:
    parser = ArgumentParser(description=f"TMTCrunch version {__version__}")
    parser.add_argument("file", nargs="+", help="Scavager *_PSMs_full.tsv files.")
    parser.add_argument(
        "--specimen-tags",
        help="Comma-separated sequence of specimen TMT tags.",
    )
    parser.add_argument("--gis-tags", help="Comma-separated sequence of GIS TMT tags.")
    parser.add_argument("--cfg", help="Path to configuration file.")
    parser.add_argument(
        "--output-dir",
        "--odir",
        default="",
        help="Existing output directory. Default is current directory.",
    )
    parser.add_argument(
        "--output-prefix",
        "--oprefix",
        default="tmtcrunch_",
        help="Prefix for output files. Default is 'tmtcrunch_'.",
    )
    parser.add_argument(
        "--keep-columns",
        action="extend",
        nargs="+",
        type=str,
        help="Extra columns from input files to keep in output files.",
    )
    parser.add_argument(
        "--verbose",
        type=int,
        choices=range(3),
        default=1,
        help="Logging verbosity. Default is 1.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{__version__}",
        help="Output version information and exit.",
    )

    cmd_args = parser.parse_args()
    log_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    logging.basicConfig(
        format="{levelname}: {message}",
        datefmt="[%H:%M:%S]",
        level=log_levels[cmd_args.verbose],
        style="{",
    )

    settings = tomllib.loads(DEFAULT_CONFIG)
    if cmd_args.cfg:
        with open(cmd_args.cfg, "rb") as f:
            user_settings = tomllib.load(f)
            settings |= user_settings
    settings = update_settings(settings, cmd_args)

    if len(settings["gis_columns"]) == 0:
        logger.error("At least one GIS column is required!")
        sys.exit(1)
    conflicting_tags = set(settings["gis_tags"]) & set(settings["specimen_tags"])
    if conflicting_tags:
        logger.error(f"Overlapping GIS and specimen TMT tags: {conflicting_tags}")
        sys.exit(1)
    if settings["groupwise"] and "target_prefixes" not in settings.keys():
        target_prefixes = []
        for group_cfg in settings["psm_group"].values():
            for prefixes in group_cfg["prefixes"]:
                target_prefixes.extend(prefixes)
        settings["target_prefixes"] = uniq(target_prefixes)
    logger.info(
        "Starting...\n"
        + f"TMTCrunch version {__version__}\n"
        + format_settings(settings)
    )
    if len(settings["gis_columns"]) == 1:
        logger.warning(
            "Only one GIS channel is specified. Using simplified quantification."
        )

    df_psm, df_protein, df_gene = process_single_batch(cmd_args.file, settings)
    for df, ext in zip([df_psm, df_protein, df_gene], ["psm", "protein", "gene"]):
        fpath = os.path.join(cmd_args.output_dir, f"{cmd_args.output_prefix}{ext}.tsv")
        logger.info(f"Saving {fpath}")
        df.to_csv(fpath, sep="\t", index=False)
    logger.info("Done.")


if __name__ == "__main__":
    cli_main()
