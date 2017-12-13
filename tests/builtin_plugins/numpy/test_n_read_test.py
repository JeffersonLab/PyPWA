import os

import pytest

from PyPWA.libs.components.data_processor import exceptions
from PyPWA.builtin_plugins.numpy import n_read_tests

NUMPY_TEST_DATA = os.path.join(
    os.path.dirname(__file__),
    "../../test_data/docs/numpy_test_data.npy"
)

NUMPY_TEST_DATA_2 = os.path.join(
    os.path.dirname(__file__), "../../test_data/docs/numpydata.npz"
)

NUMPY_TEST_DATA_3 = os.path.join(
    os.path.dirname(__file__), "../../test_data/docs/numpydata.txt"
)


NOISE_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../test_data/docs/noise_test_data"
)


CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../test_data/docs/sv_test_data.csv"
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


def test_test_fails_with_bad_files(setup_test):
    with pytest.raises(exceptions.IncompatibleData):
        setup_test.test(NOISE_TEST_DATA)


def test_test_fails_with_csv_files(setup_test):
    with pytest.raises(exceptions.IncompatibleData):
        setup_test.test(NOISE_TEST_DATA)


def test_test_passes_with_good_files(setup_test, tests_pass):
    setup_test.test(tests_pass)

