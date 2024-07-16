import os
import pandas as pd

from seq_tools import to_dna, calc_edit_distance

from construct_design.logger import get_logger
from construct_design.paths import get_py_path

log = get_logger("validate")


def is_sequence_lengths_within_range(df: pd.DataFrame) -> bool:
    """
    Checks if the lengths of sequences in the DataFrame are within an acceptable range.

    Args:
        df (pd.DataFrame): The DataFrame containing the sequences.

    Returns:
        bool: True if all sequence lengths are within the acceptable range, False otherwise.
    """
    avg_size = df["sequence"].str.len().mean()
    min_size = avg_size * 0.9
    max_size = avg_size * 1.1
    if all(df["sequence"].str.len() > min_size) and all(
        df["sequence"].str.len() < max_size
    ):
        return True
    else:
        log.warning("Sequence lengths are not within the acceptable range.")
        return False


def is_sequences_diverse_enough(df: pd.DataFrame) -> bool:
    """
    Checks if the sequences in the DataFrame are diverse enough.

    Args:
        df (pd.DataFrame): The DataFrame containing the sequences.

    Returns:
        bool: True if the sequences are diverse enough, False otherwise.
    """
    # Calculate the edit distance between all sequences
    edit_dist = calc_edit_distance(df)
    if edit_dist > 15:
        return True
    else:
        log.warning("Sequences are not diverse enough.")
        return False


def get_seq_fwd_primer_code(df: pd.DataFrame) -> str:
    """
    Returns the code for the forward primer based on the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the sequences.

    Returns:
        str: The code for the forward primer, or an empty string if no match is found.
    """
    df = df.copy()
    df = to_dna(df)
    path = os.path.join(get_py_path(), "resources", "p5_sequences.csv")
    df_p5 = pd.read_csv(path)
    for _, row in df_p5.iterrows():
        # if all sequences in df start with the p5 sequence then return the p5 code
        if all(df["sequence"].str.startswith(row["sequence"])):  # type: ignore
            return row["code"]

    return ""


def check_rt_seq(df: pd.DataFrame) -> str:
    """
    Check if all sequences in the given DataFrame end with a specific reverse
    transcription (RT) primer sequence.

    Args:
        df (pd.DataFrame): The DataFrame containing the sequences to check.

    Returns:
        str: The name of the reverse transcription sequence if all sequences in the DataFrame
            end with it, otherwise returns None.
    """
    path = os.path.join(get_py_path(), "resources", "rt_seqs.csv")
    df_p5 = pd.read_csv(path)
    name = None
    for _, row in df_p5.iterrows():
        # if all sequences in df start with the p5 sequence then return the p5 code
        if all(df["sequence"].str.endswith(row["sequence"])):  # type: ignore
            name = row["name"]
        if all(df["sequence"].str.endswith("AC" + row["sequence"])):  # type: ignore
            name = row["name"] + "_AC"
    return name
