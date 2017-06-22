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

import pytest
from PyPWA.builtin_plugins.data import exceptions
from PyPWA.builtin_plugins.data.builtin.numpy import n_read_tests

NUMPY_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../../../data/test_docs/numpy_test_data.npy"
)

NUMPY_TEST_DATA_2 = os.path.join(
    os.path.dirname(__file__), "../../../../data/test_docs/numpydata.npz"
)

NUMPY_TEST_DATA_3 = os.path.join(
    os.path.dirname(__file__), "../../../../data/test_docs/numpydata.txt"
)


NOISE_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../../../data/test_docs/noise_test_data"
)


@pytest.fixture(scope="module")
def setup_test():
    return n_read_tests.NumpyDataTest()

@pytest.fixture(
    scope="module",
    params=[
        NUMPY_TEST_DATA, NUMPY_TEST_DATA_2, NUMPY_TEST_DATA_3
    ]
)
def tests_pass(request):
    return request.param


def test_quick_test_fails_with_bad_files(setup_test):
    with pytest.raises(exceptions.IncompatibleData):
        setup_test.quick_test(NOISE_TEST_DATA)


def test_full_test_fails_with_bad_files(setup_test):
    with pytest.raises(exceptions.IncompatibleData):
        setup_test.full_test(NOISE_TEST_DATA)


def test_quick_test_passes_with_good_files(setup_test, tests_pass):
    setup_test.quick_test(tests_pass)


def test_full_test_passes_with_good_files(setup_test, tests_pass):
    setup_test.full_test(tests_pass)