from PyPWA import Path
from PyPWA.libs import misc_file_libs


ROOT = Path(__file__).parent
CSV_TEST_DATA = ROOT / "../test_data/docs/sv_test_data.csv"
GAMP_TEST_DATA = ROOT /  "../test_data/docs/gamp_test_data.gamp"
KV_TEST_DATA = ROOT / "../test_data/docs/kv_test_data.txt"
FILE_LOCATION = ROOT / "../test_data/docs/sv_test_data.tsv"


"""
Tests Cache Location
"""

def DataLocation_TestHelper(location):
    assert location.parent.exists()


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
