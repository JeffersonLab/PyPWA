import pytest

from PyPWA import Path
from PyPWA.plugins.data.kv import k_metadata

ROOT = Path(__file__).parent
KV_TEST_DATA = ROOT / "../../../test_data/docs/kv_test_data.txt"
CSV_TEST_DATA = ROOT / "../../../test_data/docs/sv_test_data.csv"
FLOAT_TEST_DATA = ROOT / "../../../test_data/docs/kv_floats_test_data.txt"


@pytest.fixture()
def data_test():
    return k_metadata._EVILDataTest()


def test_kv_data_passes(data_test):
    assert data_test.can_read(KV_TEST_DATA)


def test_csv_data_fails(data_test):
    assert not data_test.can_read(CSV_TEST_DATA)


def test_kv_data_fails(data_test):
    assert not data_test.can_read(FLOAT_TEST_DATA)
