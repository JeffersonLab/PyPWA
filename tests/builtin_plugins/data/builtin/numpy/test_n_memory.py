#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import numpy
import pytest
from PyPWA.builtin_plugins.data.builtin.numpy import n_memory

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__),
    "../../../../data/test_docs/temporary_write_data_numpy"
)

NUMPY_TEST_DATA = os.path.join(
    os.path.dirname(__file__),
    "../../../../data/test_docs/numpy_test_data.npy"
)

NUMPY_TEST_DATA_2 = os.path.join(
    os.path.dirname(__file__), "../../../../data/test_docs/numpydata.npz"
)

NUMPY_TEST_DATA_3 = os.path.join(
    os.path.dirname(__file__), "../../../../data/test_docs/numpydata.txt"
)

PF_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../../../data/test_docs/numpy_test_data.pf"
)

TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../../../data/test_docs/numpy_test_data"
)


@pytest.fixture()
def gen_noisy_single_array():
    data = numpy.arange(0, 10)
    return data


@pytest.fixture()
def gen_boolean_data():
    data = numpy.ones(10)
    return data


@pytest.fixture()
def writer_and_parser():
    return n_memory.NumpyMemory()


@pytest.fixture()
def write_noise_data(writer_and_parser, gen_noisy_single_array):
    writer_and_parser.write(NUMPY_TEST_DATA, gen_noisy_single_array)
    writer_and_parser.write(NUMPY_TEST_DATA_3, gen_noisy_single_array)
    yield gen_noisy_single_array
    os.remove(NUMPY_TEST_DATA)
    os.remove(NUMPY_TEST_DATA_3)


def test_normal_read_data(writer_and_parser, write_noise_data):
    new_data = writer_and_parser.parse(NUMPY_TEST_DATA)
    new_data_3 = writer_and_parser.parse(NUMPY_TEST_DATA_3)

    numpy.testing.assert_equal(new_data, write_noise_data)
    numpy.testing.assert_equal(new_data_3, write_noise_data)


def test_non_specified_file_case(writer_and_parser, write_noise_data):
    writer_and_parser.write(TEST_DATA, write_noise_data)


@pytest.fixture()
def write_multiple_array_data(writer_and_parser):
    array_tuple = (gen_noisy_single_array, gen_boolean_data)
    writer_and_parser.write(NUMPY_TEST_DATA_2, array_tuple)  # own test
    yield array_tuple
    os.remove(NUMPY_TEST_DATA_2)


def test_multiple_array_data(writer_and_parser, write_multiple_array_data):
    new_data_2 = writer_and_parser.parse(NUMPY_TEST_DATA_2)
    numpy.testing.assert_equal(new_data_2, write_multiple_array_data)


@pytest.fixture()
def write_bool_data(writer_and_parser, gen_boolean_data):
    writer_and_parser.write(PF_TEST_DATA, gen_boolean_data)
    yield gen_boolean_data
    os.remove(PF_TEST_DATA)


def test_bool_data(writer_and_parser, write_bool_data):
    new_data = writer_and_parser.parse(PF_TEST_DATA)
    numpy.testing.assert_equal(new_data, write_bool_data)


