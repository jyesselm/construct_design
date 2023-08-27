import pandas as pd
from construct_design.logger import get_logger

log = get_logger("PROCESSING")


def fix_column_names_in_dataframe(df):
    if "seq" in df.columns:
        log.info("Renaming seq to sequence")
        df = df.rename(columns={"seq": "sequence"})
    if "ss" in df.columns:
        log.info("Renaming ss to structure")
        df = df.rename(columns={"ss": "structure"})
    log.info("Standardizing column names. No spaces and all lowercase")
    df.columns = df.columns.str.replace(" ", "_").str.lower()
    return df
