from typing import Dict
import pandas as pd
import glob
from pathlib import Path

from construct_design.logger import get_logger

log = get_logger("PROCESSING")


def fix_column_names_in_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    standardizes column names in a dataframe. No spaces and all lowercase
    :param df: input dataframe
    :type df: pd.DataFrame
    :return: pd.Dataframe
    """
    df = df.copy()
    df.columns = df.columns.str.replace(" ", "_").str.lower()
    if "seq" in df.columns:
        log.info("Renaming seq to sequence")
        df = df.rename(columns={"seq": "sequence"})
    if "ss" in df.columns:
        log.info("Renaming ss to structure")
        df = df.rename(columns={"ss": "structure"})
    log.info("Standardizing column names. No spaces and all lowercase")
    df.columns = df.columns.str.replace(" ", "_").str.lower()
    if "name" not in df.columns:
        log.info("Adding name column in the format of seq_#")
        df["name"] = [f"seq_{x}" for x in range(len(df))]
    # make sure the most important columns are first
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
