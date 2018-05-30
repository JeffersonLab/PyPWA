import numpy
import pytest

from PyPWA import Path
from PyPWA.libs.components.data_processor import shell_interface

"""
File Locations
"""

ROOT = Path(__file__).parent
CSV_TEST_DATA = ROOT / "../../../test_data/docs/sv_test_data.csv"
TEMP_WRITE_LOCATION = ROOT / "../../../test_data/docs/temporary_write_data"


"""
Test helping functions
"""

@pytest.fixture
def parser_with_cache():
    return shell_interface.ShellDataProcessor(enable_cache=True)


@pytest.fixture
def parser_no_cache():
    return shell_interface.ShellDataProcessor(enable_cache=False)


@pytest.fixture
def array_data():
    data = numpy.zeros(5000, [("x", "f8"), ("y", "f8")])
    data["x"] = numpy.random.rand(5000)
    data["y"] = numpy.random.rand(5000)
    return data


@pytest.fixture
def clear_temp():
    yield
    TEMP_WRITE_LOCATION.unlink() if TEMP_WRITE_LOCATION.exists() else None


"""
Tests
"""

def test_read_data_matches_expected(parser_no_cache):
    data = parser_no_cache.parse(CSV_TEST_DATA)
    assert data["QFactor"][3] == 0.832133


def test_written_data_matches_read_without_cache(
        parser_no_cache, array_data, clear_temp
):
    parser_no_cache.write(TEMP_WRITE_LOCATION, array_data)
    new_data = parser_no_cache.parse(TEMP_WRITE_LOCATION)

    numpy.testing.assert_array_equal(new_data, array_data)


def test_written_data_matches_read_with_cache(
        parser_with_cache, array_data, clear_temp
):
    parser_with_cache.write(TEMP_WRITE_LOCATION, array_data)
    new_data = parser_with_cache.parse(TEMP_WRITE_LOCATION)

    numpy.testing.assert_array_equal(new_data, array_data)


def test_Iterator_ReadData_DataMatches():
    handler = shell_interface.ShellDataProcessor()
    with handler.get_reader(CSV_TEST_DATA) as reader:
        first_line = reader.next()
        assert first_line["ctAD"] == -0.265433
