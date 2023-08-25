import shutil
from tabulate import tabulate


def centered_box(text):
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


def padded_text(text):
    # Get terminal width
    columns, _ = shutil.get_terminal_size()
    columns -= 30
    # Calculate the number of dashes needed
    num_dashes = columns - len(text)
    # Create the padded string
    padded_string = text + "-" * num_dashes
    return padded_string


def library_summary(df):
    pass
