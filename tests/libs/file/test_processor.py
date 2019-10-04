import pytest

from pathlib import Path

from PyPWA.libs.file import processor
import numpy as npy

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
    data = parser.parse(CSV)
    assert isinstance(data, npy.ndarray)
    assert data.dtype.names


def test_can_read_evil(parser):
    reader = parser.get_reader(EVIL)
    data = reader.next()
    assert isinstance(data, npy.ndarray)
    assert data.dtype.names


def test_can_load_pass_fail(parser):
    data = parser.parse(BOOL)
    assert isinstance(data, npy.ndarray)
    assert data.dtype == bool
