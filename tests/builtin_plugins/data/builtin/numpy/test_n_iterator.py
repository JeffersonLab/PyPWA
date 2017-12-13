import os

import numpy
import pytest
from PyPWA.builtin_plugins.data.builtin.numpy import n_iterator


NUMPY_DATA = os.path.join(
    os.path.dirname(__file__),"../../../../data/test_docs/numpy_test_data.npy"
)

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__), "../../../../data/test_docs/temporary_write_data.npy"
)


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
    os.remove(TEMP_WRITE_LOCATION)


def test_read_data_matches_wrote(read_and_write, clear_write_location):
    file_1 = numpy.load(NUMPY_DATA)
    file_2 = numpy.load(TEMP_WRITE_LOCATION)
    numpy.testing.assert_array_equal(file_1, file_2)
