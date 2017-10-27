import pytest
import os

from PyPWA.builtin_plugins.kv import k_read_tests
from PyPWA.libs.data_handler import exceptions

KV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/kv_test_data.txt"
)

CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/sv_test_data.csv"
)

FLOAT_TEST_DATA = os.path.join(
    os.path.dirname(__file__),
    "../../data/test_docs/kv_floats_test_data.txt"
)


@pytest.fixture()
def data_test():
    return k_read_tests.EVILDataTest()


def test_kv_data_passes(data_test):
    data_test.test(KV_TEST_DATA)


def test_csv_data_fails(data_test):
    with pytest.raises(exceptions.IncompatibleData):
        data_test.test(CSV_TEST_DATA)


def test_kv_data_fails(data_test):
    with pytest.raises(exceptions.IncompatibleData):
        data_test.test(FLOAT_TEST_DATA)
