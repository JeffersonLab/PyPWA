import os

from PyPWA.libs import misc_file_libs


CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../data/test_docs/sv_test_data.csv"
)

GAMP_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../data/test_docs/gamp_test_data.gamp"
)

KV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../data/test_docs/kv_test_data.txt"
)

FILE_LOCATION = os.path.join(
    os.path.dirname(__file__),
    "../data/test_docs/sv_test_data.tsv"
)


"""
Tests Cache Location
"""

def DataLocation_TestHelper(location):
    new_location = os.path.split(location)
    assert os.path.exists(new_location[0])


def test_DataLocation_FindCache_DirectoryReturned():
    location = misc_file_libs.get_cache_uri()
    DataLocation_TestHelper(location)


"""
Tests File Hash
"""

def test_FileHash_sha512_StringReturned():
    the_hash = misc_file_libs.get_sha512_hash(FILE_LOCATION)
    check_hash(the_hash)


def check_hash(the_hash):
    assert isinstance(the_hash, str)
    assert len(the_hash) > 5


"""
Tests File Length
"""

def test_csv_data_length():
    assert misc_file_libs.get_file_length(CSV_TEST_DATA) == 5


def test_gamp_data_length():
    assert misc_file_libs.get_file_length(GAMP_TEST_DATA) == 36


def test_kv_data_length():
    assert misc_file_libs.get_file_length(KV_TEST_DATA) == 10
