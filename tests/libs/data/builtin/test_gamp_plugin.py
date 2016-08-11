import os

import pytest
import numpy

from PyPWA.libs.data import exceptions
from PyPWA.libs.data import data_templates
from PyPWA.libs.data.builtin import gamp

CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "test_docs/sv_test_data.csv"
)

GAMP_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "test_docs/gamp_test_data.gamp"
)

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__), "test_docs/temporary_write_data"
)


def test_Validator_CheckGAMPValid_TestPass():
    """
    Checks that the validator correctly identifies a GAMP file.
    """
    validator = gamp.GampDataPlugin()
    validator.read_test(GAMP_TEST_DATA)


def test_Validator_CheckCSVValid_TestFail():
    """
    Checks that the validator correctly fails if the file is not a GAMP
    file.
    """
    validator = gamp.GampDataPlugin()

    with pytest.raises(exceptions.IncompatibleData):
        validator.read_test(CSV_TEST_DATA)


def test_GAMPMemory_ParseKnownData_DataMatches():
    """
    Checks that data read in from the file matches what is known.
    """
    parser = gamp.GampMemory()
    data = parser.parse(GAMP_TEST_DATA)
    assert len(data) == 6
    assert data[0][0][4] == 3.90355
    assert data[5][4][5] == 0.549938


def test_GAMPMemory_LoopingKnownData_DataMatches():
    """
    Checks that data written out and read back in matches what we
    expected.
    """
    rendered = gamp.GampMemory()
    data = rendered.parse(GAMP_TEST_DATA)
    rendered.write(TEMP_WRITE_LOCATION, data)

    assert os.path.exists(TEMP_WRITE_LOCATION)
    new_data = rendered.parse(TEMP_WRITE_LOCATION)

    numpy.testing.assert_array_equal(data, new_data)
    os.remove(TEMP_WRITE_LOCATION)
