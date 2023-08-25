import pytest
import os
import pandas as pd

from construct_design.processing import fix_secondary_structures_from_rnamake

# get current directory to use as resource directory
RESOURCE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/resources/"


def test_fix_secondary_structures_from_rnamake():
    df = pd.read_csv(RESOURCE_DIR + "designs.csv")
    df = df.rename(
        columns={"design_structure": "structure", "design_sequence": "sequence"}
    )
    df = fix_secondary_structures_from_rnamake(df)
    assert df.iloc[0]["structure"].find("(..(.)") == -1
