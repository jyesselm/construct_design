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


def fix_secondary_structures_from_rnamake(df):
    log.info("fixing secondary structures that rnamake messed up")
    if "structure" not in df.columns:
        log.error("No structure column in dataframe")
        return df
    count = 0
    for i, row in df.iterrows():
        structure = row["structure"]
        if structure.find("(..(.)") == -1:
            continue
        structure = structure.replace("(..(.)", "(....)")
        sequence = row["sequence"]
        left_pos = sequence[0:20].find("UAUGG")
        right_pos = sequence.find("CCUAAG")
        if left_pos == -1 or right_pos == -1:
            log.error(f"Could not find receptor in sequence for {sequence}")
            continue
        structure = list(structure)
        structure[left_pos : left_pos + 5] = "(..(("
        structure[right_pos : right_pos + 6] = "))...)"
        df.at[i, "structure"] = "".join(structure)
        count += 1
    log.info(f"fixed {count}/{len(df)} structures")
    return df
