import pandas as pd

from construct_design.logger import get_logger
from construct_design.paths import get_lib_path

log = get_logger("validate")


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
    path = os.path.join(get_lib_path(), "resources", "p5_sequences.csv")
    df_p5 = pd.read_csv(path)
    for _, row in df_p5.iterrows():
        # if all sequences in df start with the p5 sequence then return the p5 code
        if all(df["sequence"].str.startswith(row["sequence"])):  # type: ignore
            return row["code"]
    return ""
