import numpy
import pytest

from PyPWA import Path
from PyPWA.builtin_plugins.numpy import n_memory

TEMP_WRITE_LOCATION = Path("temporary_write_data_numpy")
NUMPY_TEST_DATA = Path("numpy_test_data.npy")
NUMPY_TEST_DATA_2 = Path("numpydata.npz")
NUMPY_TEST_DATA_3 = Path("numpydata.txt")
PF_TEST_DATA = Path("numpy_test_data.pf")
TEST_DATA = Path("numpy_unspec_data")


@pytest.fixture(scope="module")
def gen_noisy_single_array():
    data = numpy.arange(0, 10)
    return data


@pytest.fixture(scope="module")
def gen_boolean_data():
    data = numpy.random.choice([True, False], 10)
    return data


@pytest.fixture()
def writer_and_parser():
    return n_memory.NumpyMemory()


@pytest.fixture(params=[NUMPY_TEST_DATA, NUMPY_TEST_DATA_3])
def write_noise_data(request, writer_and_parser, gen_noisy_single_array):
    writer_and_parser.write(request.param, gen_noisy_single_array)
    yield gen_noisy_single_array, request.param
    request.param.unlink()


def test_normal_read_data(writer_and_parser, write_noise_data):
    new_data = writer_and_parser.parse(write_noise_data[1])
    numpy.testing.assert_equal(new_data, write_noise_data[0])


def test_non_specified_file_case(writer_and_parser, gen_noisy_single_array):
    writer_and_parser.write(TEST_DATA, gen_noisy_single_array)
    Path("numpy_unspec_data.npy").unlink()


@pytest.fixture()
def write_bool_data(writer_and_parser, gen_boolean_data):
    writer_and_parser.write(PF_TEST_DATA, gen_boolean_data)
    yield gen_boolean_data
    PF_TEST_DATA.unlink()

def test_bool_data(writer_and_parser, write_bool_data):
    new_data = writer_and_parser.parse(PF_TEST_DATA)
    numpy.testing.assert_equal(new_data, write_bool_data)
    assert new_data.dtype == bool
