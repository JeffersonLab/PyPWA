import io

import os

from PyPWA.core import tools

FILE_LOCATION = os.path.join(
    os.path.dirname(__file__),
    "../builtin_plugins/data/builtin/test_docs/sv_test_data.tsv"
)

data_loc = tools.DataLocation()
test_file = io.open(FILE_LOCATION, "br")
hashing = tools.FileHashString()


def DataLocation_TestHelper(location):
    """
    Simple wrapper around tests for DataLocation.
    Checks if the path to the returned file exists.

    Args:
        location (str): The path to file.
    """
    new_location = os.path.split(location)
    assert os.path.exists(new_location[0])


def test_DataLocation_FindCache_DirectoryReturned():
    location = data_loc.get_cache_uri("here.cache")
    DataLocation_TestHelper(location)


def test_DataLocation_FindData_DirectoryReturned():
    location = data_loc.get_data_uri("here.data")
    DataLocation_TestHelper(location)


def test_DataLocation_FindLog_DirectoryReturned():
    location = data_loc.get_log_uri("here.log")
    DataLocation_TestHelper(location)


def test_DataLocation_FindConfig_DirectoryReturned():
    location = data_loc.get_config_uri("here")
    DataLocation_TestHelper(location)


def test_FileHash_md5_StringReturned():
    the_hash = hashing.get_md5_hash(test_file)

    assert isinstance(the_hash, str)
    assert len(the_hash) > 5


def test_FileHash_sha1_StringReturned():
    the_hash = hashing.get_sha1_hash(test_file)

    assert isinstance(the_hash, str)
    assert len(the_hash) > 5


def test_FileHash_sha224_StringReturned():
    the_hash = hashing.get_sha224_hash(test_file)

    assert isinstance(the_hash, str)
    assert len(the_hash) > 5


def test_FileHash_sha256_StringReturned():
    the_hash = hashing.get_sha256_hash(test_file)

    assert isinstance(the_hash, str)
    assert len(the_hash) > 5


def test_FileHash_sha384_StringReturned():
    the_hash = hashing.get_sha384_hash(test_file)

    assert isinstance(the_hash, str)
    assert len(the_hash) > 5


def test_FileHash_sha512_StringReturned():
    the_hash = hashing.get_sha512_hash(test_file)

    assert isinstance(the_hash, str)
    assert len(the_hash) > 5
