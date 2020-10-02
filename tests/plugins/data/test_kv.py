from pathlib import Path

import pytest

from PyPWA.plugins.data import kv

ROOT = (Path(__file__).parent / "../../test_data/docs").resolve()

TEMP_LOCATION = ROOT / "temporary_write_data"

GOOD_DATA = [
    ROOT / "set1.kvars",
    ROOT / "set2.kvars"
]

BAD_DATA = [
    ROOT / "set1.csv",
    ROOT / "set2.npy",
    ROOT / "bad_set.kvars"
]


@pytest.fixture
def parser():
    return kv.metadata.get_memory_parser()


@pytest.fixture
def iterator():
    return {
        "reader": kv.metadata.get_reader,
        "writer": kv.metadata.get_writer
    }


@pytest.fixture
def can_read():
    return kv.metadata.get_read_test()


@pytest.fixture(params=GOOD_DATA)
def good_data(request):
    return request.param


def test_can_read_known_good_data(good_data, can_read):
    assert can_read.can_read(good_data)


def test_parser_and_writer(parser, structured_data, check_memory_read_write):
    check_memory_read_write(parser, structured_data, TEMP_LOCATION)


def test_iterator_does_not_copy_data(
        iterator, structured_data, check_iterator_passes_data
):
    assert check_iterator_passes_data(iterator["reader"](GOOD_DATA[0], False))


def test_iterator_with_numpy_arrays(
        iterator, structured_data, iterate_numpy_arrays
):
    iterate_numpy_arrays(iterator, structured_data, TEMP_LOCATION)


def test_iterator_with_pandas_dataframe(
        iterator, structured_data, iterate_dataframe
):
    iterate_dataframe(iterator, structured_data, TEMP_LOCATION)