import numpy
import pytest

from PyPWA import Path
from PyPWA.plugins.data.gamp import g_process, g_metadata


ROOT = Path(__file__).parent
CSV_TEST_DATA = ROOT / "../../test_data/docs/sv_test_data.csv"
GAMP_TEST_DATA = ROOT / "../../test_data/docs/gamp_test_data.gamp"
TEMP_WRITE_LOCATION = ROOT / "../../test_data/docs/temporary_write_data"


def test_Validator_CheckGAMPValid_TestPass():
    """
    Checks that the validator correctly identifies a GAMP file.
    """
    validator = g_metadata._GampDataTest()
    assert validator.can_read(GAMP_TEST_DATA)


def test_Validator_CheckCSVValid_TestFail():
    """
    Checks that the validator correctly fails if the file is not a GAMP
    file.
    """
    validator = g_metadata._GampDataTest()
    assert not validator.can_read(CSV_TEST_DATA)


def test_GAMPMemory_ParseKnownData_DataMatches():
    """
    Checks that data read in from the file matches what is known.
    """
    parser = g_process.GampMemory()
    data = parser.parse(GAMP_TEST_DATA, numpy.float64)
    assert data.event_count == 6
    assert data[0][0].z == 3.90355
    assert data[4][5].e == 0.549938


def test_GAMPMemory_LoopingKnownData_DataMatches():
    """
    Checks that data written out and read back in matches what we
    expected.
    """
    rendered = g_process.GampMemory()
    data = rendered.parse(GAMP_TEST_DATA, numpy.float64)
    rendered.write(TEMP_WRITE_LOCATION, data)

    assert TEMP_WRITE_LOCATION.exists()
    new_data = rendered.parse(TEMP_WRITE_LOCATION, numpy.float64)

    numpy.testing.assert_array_equal(
        data[0].get_array(),
        new_data[0].get_array()
    )
    TEMP_WRITE_LOCATION.unlink()
