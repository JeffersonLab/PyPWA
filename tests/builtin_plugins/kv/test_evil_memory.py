import os

import numpy
import pytest

from PyPWA.builtin_plugins.kv import k_memory

TEMP_WRITE_LOCATION = "temporary_write_data"


@pytest.fixture(scope='module')
def random_numpy_data():
    noise = numpy.zeros(20, dtype=[('x', 'f8'), ('y', 'f8')])
    noise['x'] = numpy.random.rand(20)
    noise['y'] = numpy.random.rand(20)
    return noise


@pytest.fixture()
def parser():
    return k_memory.EVILMemory()


@pytest.fixture()
def write_temp_data(parser, random_numpy_data):
    parser.write(TEMP_WRITE_LOCATION, random_numpy_data)
    yield parser.parse(TEMP_WRITE_LOCATION)
    os.remove(TEMP_WRITE_LOCATION)


def test_wrote_data_matches(write_temp_data, random_numpy_data):
    numpy.testing.assert_array_equal(write_temp_data, random_numpy_data)
