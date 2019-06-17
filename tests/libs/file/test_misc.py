from pathlib import Path
from PyPWA.libs.file import misc


ROOT = (Path(__file__).parent / "../../test_data/docs").resolve()
SET1 = ROOT / "set1.csv"
SET2 = ROOT / "set2.kvars"


"""
Tests Cache Location
"""


def test_cache_directory_exists():
    location = misc.get_cache_uri()
    assert location.parent.exists()


"""
Tests File Hash
"""


def test_hash_is_string():
    the_hash = misc.get_sha512_hash(SET1)
    assert isinstance(the_hash, str)
    assert len(the_hash) != 0  # We don't want an empty string


"""
Tests File Length
"""


def test_file_length_set1_csv():
    assert misc.get_file_length(SET1) == 1001


def test_file_length_set2_kvars():
    assert misc.get_file_length(SET2) == 12
