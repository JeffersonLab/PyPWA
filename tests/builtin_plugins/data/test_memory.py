import os

import numpy
import pytest

from PyPWA.builtin_plugins.data import memory

CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/sv_test_data.csv"
)

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/temporary_write_data"
)


@pytest.fixture
def parser_with_cache():
    def raise_error(file_location):
        raise RuntimeError("Cache was not loaded!")

    mem = memory.Memory(options={"enable cache": True})
    mem._read_data = raise_error

    return mem


@pytest.fixture
def parser_no_cache():
    return memory.Memory(enable_cache=False)


@pytest.fixture
def array_data():
    data = numpy.zeros(5000, [("x", "f8"), ("y", "f8")])
    data["x"] = numpy.random.rand(5000)
    data["y"] = numpy.random.rand(5000)
    return data


@pytest.fixture
def clear_temp():
    yield
    try:
        os.remove(TEMP_WRITE_LOCATION)
    except (OSError, IOError):
        pass


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