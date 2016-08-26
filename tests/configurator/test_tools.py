import os

from PyPWA.configurator import tools

data_loc = tools.DataLocation()
hashing = tools.FileHash()

test_file = open(tools.__file__, "r")


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
    location = data_loc.find_cache_dir("here", ".cache")
    DataLocation_TestHelper(location)


def test_DataLocation_FindData_DirectoryReturned():
    location = data_loc.find_data_dir("here", ".data")
    DataLocation_TestHelper(location)


def test_DataLocation_FindLog_DirectoryReturned():
    location = data_loc.find_log_dir("here", ".log")
    DataLocation_TestHelper(location)


def test_DataLocation_FindConfig_DirectoryReturned():
    location = data_loc.find_config_dir("here")
    DataLocation_TestHelper(location)


def test_FileHash_md5_StringReturned():
    test_file.seek(0)
    the_hash = hashing.hash_md5(test_file)
    test_file.seek(0)

    assert isinstance(the_hash, str)
    assert len(the_hash) > 5


def test_FileHash_sha1_StringReturned():
    test_file.seek(0)
    the_hash = hashing.hash_sha1(test_file)
    test_file.seek(0)

    assert isinstance(the_hash, str)
    assert len(the_hash) > 5


def test_FileHash_sha224_StringReturned():
    test_file.seek(0)
    the_hash = hashing.hash_sha224(test_file)
    test_file.seek(0)

    assert isinstance(the_hash, str)
    assert len(the_hash) > 5


def test_FileHash_sha256_StringReturned():
    test_file.seek(0)
    the_hash = hashing.hash_sha256(test_file)
    test_file.seek(0)

    assert isinstance(the_hash, str)
    assert len(the_hash) > 5


def test_FileHash_sha384_StringReturned():
    test_file.seek(0)
    the_hash = hashing.hash_sha384(test_file)
    test_file.seek(0)

    assert isinstance(the_hash, str)
    assert len(the_hash) > 5


def test_FileHash_sha512_StringReturned():
    test_file.seek(0)
    the_hash = hashing.hash_sha512(test_file)
    test_file.seek(0)

    assert isinstance(the_hash, str)
    assert len(the_hash) > 5
