import numpy
import pytest

from PyPWA import Path
from PyPWA.plugins.data.numpy import n_process

PARENT = Path(__file__).parent
TEMP_WRITE_LOCATION = Path("temporary_write_data_numpy.npy")
NUMPY_TEST_DATA = Path("numpy_test_data.npy")
NUMPY_TEST_DATA_2 = Path("numpydata.npz")
NUMPY_TEST_DATA_3 = Path("numpydata.txt")
PF_TEST_DATA = Path("numpy_test_data.pf")
TEST_DATA = Path("numpy_unspec_data")
NUMPY_DATA = PARENT / "../../../test_data/docs/numpy_test_data.npy"


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
    return n_process.NumpyMemory()


@pytest.fixture(params=[NUMPY_TEST_DATA, NUMPY_TEST_DATA_3])
def write_noise_data(request, writer_and_parser, gen_noisy_single_array):
    writer_and_parser.write(request.param, gen_noisy_single_array)
    yield gen_noisy_single_array, request.param
    request.param.unlink()


def test_normal_read_data(writer_and_parser, write_noise_data):
    new_data = writer_and_parser.parse(write_noise_data[1], numpy.float64)
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
    new_data = writer_and_parser.parse(PF_TEST_DATA, numpy.float64)
    numpy.testing.assert_equal(new_data, write_bool_data)
    assert new_data.dtype == bool


@pytest.fixture()
def read_and_write():
    with n_process.NumpyReader(NUMPY_DATA, numpy.float64) as stream:
        with n_process.NumpyWriter(TEMP_WRITE_LOCATION) as writer:
            for event in stream:
                writer.write(event)
            writer.close()


@pytest.fixture
def clear_write_location():
    yield
    TEMP_WRITE_LOCATION.unlink()


def test_read_data_matches_wrote(read_and_write, clear_write_location):
    file_1 = numpy.load(str(NUMPY_DATA))
    file_2 = numpy.load(str(TEMP_WRITE_LOCATION))
    numpy.testing.assert_array_equal(file_1, file_2)
