import numpy
import pytest

from PyPWA import Path
from PyPWA.plugins.data.kv import k_process

TEMP_WRITE_LOCATION = Path("temporary_write_data")


@pytest.fixture(scope='module')
def random_numpy_data():
    noise = numpy.zeros(20, dtype=[('x', 'f8'), ('y', 'f8')])
    noise['x'] = numpy.random.rand(20)
    noise['y'] = numpy.random.rand(20)
    return noise


@pytest.fixture()
def parser():
    return k_process.EVILMemory()


@pytest.fixture()
def write_temp_data(parser, random_numpy_data):
    parser.write(TEMP_WRITE_LOCATION, random_numpy_data)
    yield parser.parse(TEMP_WRITE_LOCATION, numpy.float64)
    TEMP_WRITE_LOCATION.unlink()


def test_wrote_data_matches(write_temp_data, random_numpy_data):
    numpy.testing.assert_array_equal(write_temp_data, random_numpy_data)
