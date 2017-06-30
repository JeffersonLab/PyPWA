import os

import numpy
import pytest

from PyPWA.builtin_plugins.data import exceptions
from PyPWA.builtin_plugins.data.builtin.gamp import g_iterator
from PyPWA.builtin_plugins.data.builtin.gamp import g_memory
from PyPWA.builtin_plugins.data.builtin.gamp import g_read_tests

CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../../data/test_docs/sv_test_data.csv"
)

GAMP_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../../data/test_docs/gamp_test_data.gamp"
)

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__), "../../../data/test_docs/temporary_write_data"
)


def test_Validator_CheckGAMPValid_TestPass():
    """
    Checks that the validator correctly identifies a GAMP file.
    """
    validator = g_read_tests.GampDataTest()
    validator.test(GAMP_TEST_DATA)


def test_Validator_CheckCSVValid_TestFail():
    """
    Checks that the validator correctly fails if the file is not a GAMP
    file.
    """
    validator = g_read_tests.GampDataTest()

    with pytest.raises(exceptions.IncompatibleData):
        validator.test(CSV_TEST_DATA)


def test_GAMPMemory_ParseKnownData_DataMatches():
    """
    Checks that data read in from the file matches what is known.
    """
    parser = g_memory.GampMemory()
    data = parser.parse(GAMP_TEST_DATA)
    assert len(data) == 6
    assert data[0][0][4] == 3.90355
    assert data[5][4][5] == 0.549938


def test_GAMPMemory_LoopingKnownData_DataMatches():
    """
    Checks that data written out and read back in matches what we
    expected.
    """
    rendered = g_memory.GampMemory()
    data = rendered.parse(GAMP_TEST_DATA)
    rendered.write(TEMP_WRITE_LOCATION, data)

    assert os.path.exists(TEMP_WRITE_LOCATION)
    new_data = rendered.parse(TEMP_WRITE_LOCATION)

    numpy.testing.assert_array_equal(data, new_data)
    os.remove(TEMP_WRITE_LOCATION)


def test_GAMPReader_ResetReader_NoFail():
    reader = g_iterator.GampReader(GAMP_TEST_DATA)
    reader.reset()
