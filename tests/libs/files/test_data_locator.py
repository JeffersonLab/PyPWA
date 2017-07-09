import os

from PyPWA.libs.files import data_locator


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
