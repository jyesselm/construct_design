import pytest
import os
import pandas as pd

from construct_design.preprocessing import *

# get current directory to use as resource directory
RESOURCE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/resources/"


def test_fix_column_names_in_dataframe():
    df = pd.read_csv(RESOURCE_DIR + "non_standard_1.csv")
    df_new = fix_column_names_in_dataframe(df)
    df_new.columns.to_list() == ["name", "sequence", "structure"]


def test_get_dataframes_from_directory():
    dfs = get_dataframes_from_directory(RESOURCE_DIR)
    assert len(dfs) == 2
    assert "non_standard_1" in dfs
    assert "non_standard_2" in dfs
    assert len(dfs["non_standard_1"]) == 5
    assert len(dfs["non_standard_2"]) == 5
