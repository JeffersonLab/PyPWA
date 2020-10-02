from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from PyPWA.plugins.data import numpy

ROOT = (Path(__file__).parent / "../../test_data/docs").resolve()

TEMP_LOCATION = ROOT / "temporary_write_data.npy"

GOOD_DATA = [
    ROOT / "set1.txt",
    ROOT / "set1.pf",
    ROOT / "set1.npy",
    ROOT / "set2.txt",
    ROOT / "set2.pf",
    ROOT / "set2.npy"
]

BAD_DATA = [
    ROOT / "bad_set.txt",
    ROOT / "set1.kvars",
    ROOT / "set2.csv"
]


@pytest.fixture
def parser():
    return numpy.metadata.get_memory_parser()


@pytest.fixture
def iterator():
    return {
        "reader": numpy.metadata.get_reader,
        "writer": numpy.metadata.get_writer
    }


@pytest.fixture
def can_read():
    return numpy.metadata.get_read_test()


@pytest.fixture(params=GOOD_DATA)
def good_data(request):
    return request.param


def test_can_read_known_good_data(good_data, can_read):
    assert can_read.can_read(good_data)


def test_parser_and_writer(parser, structured_data, check_memory_read_write):
    check_memory_read_write(parser, structured_data, TEMP_LOCATION)


def test_iterator_with_numpy_arrays(
        iterator, structured_data, iterate_numpy_arrays
):
    iterate_numpy_arrays(iterator, structured_data, TEMP_LOCATION)


def test_iterator_with_pandas_dataframe(
        iterator, structured_data, iterate_dataframe
):
    iterate_dataframe(iterator, structured_data, TEMP_LOCATION)


def test_numpy_read_and_write_pf():
    pf_file = Path(TEMP_LOCATION.stem + ".pf")
    pass_fail = np.random.choice([True, False], 1000)

    numpy.metadata.get_memory_parser().write(pf_file, pass_fail)
    read = numpy.metadata.get_memory_parser().parse(pf_file)
    pf_file.unlink()

    np.testing.assert_array_equal(read, pass_fail)


def test_numpy_read_and_write_floats():
    float_file = Path(TEMP_LOCATION.stem + ".txt")
    floats = np.random.random(1000)

    numpy.metadata.get_memory_parser().write(float_file, floats)
    read = numpy.metadata.get_memory_parser().parse(float_file)
    float_file.unlink()

    np.testing.assert_array_equal(floats, read)


@pytest.fixture(scope="module")
def numpy_and_pandas():
    data = np.zeros(30, [(name, "f8") for name in ['x', 'y', 'z']])
    for column in data.dtype.names:
        data[column] = np.random.rand(30)
    return data, pd.DataFrame(data)


def test_numpy_reader_and_writer(numpy_and_pandas):
    npy_file = Path(TEMP_LOCATION.stem + ".npy")
    data = numpy_and_pandas[1][:100]

    with numpy.metadata.get_writer(npy_file) as writer:
        for index, event in data.iterrows():
            writer.write(event)

    with numpy.metadata.get_reader(npy_file, True) as reader:
        for index, event in enumerate(reader):
            pd.testing.assert_series_equal(data.iloc[index], event)

    npy_file.unlink()

