import numpy
import pytest

from PyPWA import Path
from PyPWA.builtin_plugins.numpy import n_iterator

NUMPY_DATA = Path(__file__).parent / "../../test_data/docs/numpy_test_data.npy"
TEMP_WRITE_LOCATION = Path("temp_location.npy")


@pytest.fixture()
def read_and_write():
    with n_iterator.NumpyReader(NUMPY_DATA) as stream:
        with n_iterator.NumpyWriter(TEMP_WRITE_LOCATION) as writer:
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
