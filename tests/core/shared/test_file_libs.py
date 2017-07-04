import os

from PyPWA.core.shared import file_libs


CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/sv_test_data.csv"
)

GAMP_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/gamp_test_data.gamp"
)

KV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/kv_test_data.txt"
)


def test_csv_data_length():
    assert file_libs.get_file_length(CSV_TEST_DATA) == 5


def test_gamp_data_length():
    assert file_libs.get_file_length(GAMP_TEST_DATA) == 36


def test_kv_data_length():
    assert file_libs.get_file_length(KV_TEST_DATA) == 10
