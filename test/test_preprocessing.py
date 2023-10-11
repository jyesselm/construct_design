import pytest
import os
import pandas as pd

from construct_design.preprocessing import fix_secondary_structures_from_rnamake

# get current directory to use as resource directory
RESOURCE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/resources/"
