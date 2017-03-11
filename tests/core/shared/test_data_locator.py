import os

from PyPWA.core.shared import data_locator


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
    location = data_locator.get_cache_uri()
    DataLocation_TestHelper(location)


def test_DataLocation_FindData_DirectoryReturned():
    location = data_locator.get_data_uri()
    DataLocation_TestHelper(location)


def test_DataLocation_FindLog_DirectoryReturned():
    location = data_locator.get_log_uri()
    DataLocation_TestHelper(location)


def test_DataLocation_FindConfig_DirectoryReturned():
    location = data_locator.get_config_uri()
    DataLocation_TestHelper(location)
