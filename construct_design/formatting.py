import shutil
import os
import sys
import functools
import pandas as pd
from tabulate import tabulate

from seq_tools.dataframe import calc_edit_distance

from construct_design.logger import get_logger, setup_logging


log = get_logger("formatting")


def log_and_setup(func):
    """
    Decorator to set up logging and log the start and end of the function execution.

    Args:
        func (callable): The function to wrap.

    Returns:
        callable: The wrapped function with logging and setup.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        os.makedirs("logs", exist_ok=True)
        if os.path.exists(f"logs/{func_name}.log"):
            os.remove(f"logs/{func_name}.log")
        setup_logging(file_name=f"logs/{func_name}.log")
        log.info("Ran at commandline as: %s", " ".join(sys.argv))
        log.info("\n" + centered_box(func_name.upper()))
        log.info("starting time: %s" % pd.Timestamp.now())
        try:
            result = func(*args, **kwargs)
        finally:
            log.info(f"{func_name} execution completed.")
            print("-" * 80)
        return result

    return wrapper


def centered_box(text: str) -> str:
    """Creates a centered box with the given text.

    Args:
        text (str): The text to be displayed in the centered box.

    Returns:
        str: The centered box as a string.

    """
    # Get terminal size
    columns, rows = shutil.get_terminal_size()
    columns -= 30
    # Create top border
    txt = "+" + "-" * (columns - 2) + "+\n"
    # Calculate padding for text
    total_padding = rows - 2  # Subtracting for top and bottom borders
    top_padding = total_padding // 2
    bottom_padding = total_padding - top_padding
    # Print centered text
    text_padding_left = (columns - len(text) - 2) // 2
    text_padding_right = columns - len(text) - 2 - text_padding_left
    txt += "|" + " " * text_padding_left + text + " " * text_padding_right + "|\n"
    # Create bottom border
    txt += "+" + "-" * (columns - 2) + "+\n"
    return txt


def padded_text(text: str) -> str:
    """Pads the given text with dashes to fit the terminal width.

    Args:
        text (str): The text to be padded.

    Returns:
        str: The padded string.
    """
    # Get terminal width
    columns, _ = shutil.get_terminal_size()
    columns -= 30
    # Calculate the number of dashes needed
    num_dashes = columns - len(text)
    # Create the padded string
    padded_string = text + "-" * num_dashes
    log.info(f"Padded text: {padded_string}")
    return padded_string


def libraries_table(dfs, names, edit_dist=False):
    data = []
    i = 0
    saved_df = None
    for df in dfs:
        saved_df = df
        current_data = [
            names[i],
            len(df),
            df["sequence"].str.len().mean(),
            df["sequence"].str.len().min(),
            df["sequence"].str.len().max(),
        ]
        if "ens_defect" in df.columns:
            current_data.append(df["ens_defect"].mean())
            current_data.append(df["ens_defect"].min())
            current_data.append(df["ens_defect"].max())
        if edit_dist:
            current_data.append(calc_edit_distance(df))
        data.append(current_data)
        i += 1
    headers = [
        "name",
        "# seqs",
        "avg len",
        "min len",
        "max len",
    ]
    if "ens_defect" in saved_df.columns:
        headers.extend(
            [
                "avg ens_defect",
                "min ens_defect",
                "max ens_defect",
            ]
        )
    if edit_dist:
        headers.append("edit_dist")
    return tabulate(data, headers=headers)
