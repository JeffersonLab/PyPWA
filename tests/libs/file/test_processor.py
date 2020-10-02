from pathlib import Path

import pandas as pd
import numpy as np
import pytest

from PyPWA.libs.file import processor

DATA_DIR = (Path(__file__).parent / "../../test_data/docs").resolve()
CSV = DATA_DIR / "set1.csv"
EVIL = DATA_DIR / "set1.kvars"
BOOL = DATA_DIR / "set1.pf"
GAMP = DATA_DIR / "large.gamp"


"""
We actually check that all the plugins load the write data in
tests/plugins/data. All these tests are for is to ensure that the 
data processor selects the right plugin for each of the known types.
"""


@pytest.fixture
def parser():
    return processor.DataProcessor(False, False)


def test_can_load_csv(parser):
    assert isinstance(parser.parse(CSV), np.ndarray)
    assert isinstance(parser.parse(CSV, True), pd.DataFrame)


def test_can_read_evil(parser):
    with parser.get_reader(EVIL) as reader:
        assert isinstance(next(reader), np.void)

    with parser.get_reader(EVIL, True) as reader:
        assert isinstance(next(reader), pd.Series)


def test_can_load_pass_fail(parser):
    assert isinstance(parser.parse(BOOL, True), pd.Series)
    assert parser.parse(BOOL, True).dtype == bool
    assert isinstance(parser.parse(BOOL), np.ndarray)
    assert parser.parse(BOOL).dtype == bool
