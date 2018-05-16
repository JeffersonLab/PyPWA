import pytest

from PyPWA import Path
from PyPWA.builtin_plugins.kv import k_read_tests
from PyPWA.libs.components.data_processor import exceptions

ROOT = Path(__file__).parent
KV_TEST_DATA = ROOT / "../../test_data/docs/kv_test_data.txt"
CSV_TEST_DATA = ROOT / "../../test_data/docs/sv_test_data.csv"
FLOAT_TEST_DATA = ROOT / "../../test_data/docs/kv_floats_test_data.txt"


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
