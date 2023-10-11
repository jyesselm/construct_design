from typing import Dict
import pandas as pd
import glob
from pathlib import Path

from construct_design.logger import get_logger

log = get_logger("PROCESSING")


def fix_column_names_in_dataframe(df):
    df.columns = df.columns.str.replace(" ", "_").str.lower()
    if "seq" in df.columns:
        log.info("Renaming seq to sequence")
        df = df.rename(columns={"seq": "sequence"})
    if "ss" in df.columns:
        log.info("Renaming ss to structure")
        df = df.rename(columns={"ss": "structure"})
    log.info("Standardizing column names. No spaces and all lowercase")
    df.columns = df.columns.str.replace(" ", "_").str.lower()
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
