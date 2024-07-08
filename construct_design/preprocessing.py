from typing import Dict
import pandas as pd
import glob
from pathlib import Path

from construct_design.logger import get_logger

log = get_logger("preprocessing")


def fix_column_names_in_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes column names in a dataframe.

    Replaces spaces with underscores and converts to lowercase.
    Renames specific columns if they exist. Adds a 'name' column if it doesn't exist.
    Moves the most important columns to the front.

    Args:
        df (pd.DataFrame): Input dataframe.

    Returns:
        pd.DataFrame: Dataframe with standardized column names.
    """
    df = df.copy()
    # Standardize column names
    df.columns = df.columns.str.replace(" ", "_").str.lower()
    # Rename specific columns if they exist
    if "seq" in df.columns:
        log.info("Renaming 'seq' to 'sequence'")
        df = df.rename(columns={"seq": "sequence"})
    if "ss" in df.columns:
        log.info("Renaming 'ss' to 'structure'")
        df = df.rename(columns={"ss": "structure"})

    log.info(
        "Standardizing column names. Replacing spaces with underscores and converting to lowercase."
    )
    df.columns = df.columns.str.replace(" ", "_").str.lower()

    # Add 'name' column if it doesn't exist
    if "name" not in df.columns:
        log.info("Adding 'name' column in the format of 'seq_#'")
        df["name"] = [f"seq_{x}" for x in range(len(df))]

    # Move the most important columns to the front
    columns_to_move = ["name", "sequence", "structure"]
    df = df[columns_to_move + [col for col in df.columns if col not in columns_to_move]]

    return df


def get_dataframes_from_directory(path) -> Dict[str, pd.DataFrame]:
    """
    gets all dataframes from a directory based on csvs. Returns as a dictionary
    with the name of the csv as the key and the dataframe as the value

    :param path: path to directory
    """
    log.info(f"Getting dataframes from {path}")
    csvs = glob.glob(f"{path}/*.csv")
    log.info(f"{path} contains {len(csvs)} csv files")
    dfs = {}
    for csv in csvs:
        name = Path(csv).stem
        df = pd.read_csv(csv)
        log.info(f"Reading {csv}")
        log.info(f"{name}: contains {len(df)} rows")
        log.info(f"{name}: contains columns [{' '.join(df.columns.to_list())}]")
        dfs[name] = df
    if len(dfs) == 0:
        log.error(f"No csv files found in {path}")
    return dfs


def get_rld_dataframes_from_directory(path) -> Dict[str, pd.DataFrame]:
    """
    gets all dataframes from a directory based on csvs. Returns as a dictionary
    with the name of the csv as the key and the dataframe as the value

    :param path: path to directory
    """
    log.info(f"Getting dataframes from {path}")
    csvs = glob.glob(f"{path}/*/results-rna.csv")
    log.info(f"{path} contains {len(csvs)} csv files")
    dfs = {}
    for csv in csvs:
        name = Path(csv).parent.stem
        df = pd.read_csv(csv)
        log.info(f"Reading {csv}")
        log.info(f"{name}: contains {len(df)} rows")
        log.info(f"{name}: contains columns [{' '.join(df.columns.to_list())}]")
        df = fix_column_names_in_dataframe(df)
        dfs[name] = df
    return dfs
