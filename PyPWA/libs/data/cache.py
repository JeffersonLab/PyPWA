#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Memory Caching

The objects in this file are dedicated to saving and writing chunks of memory
to file for quick loading when the data is loaded into memory again.
"""

import hashlib
import io
import logging
import pickle

from PyPWA.configuratr import tools, definitions, data_types
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class MemoryCache(object):
    def __init__(self):
        """
        Just like the old one, but new!

        This object caches data stored in the memory on disk in a format that
        can be quickly loaded too and from disk to RAM quickly. Also contains
        logic that will help determine if the the contents of the file has
        changed from the last cache.
        """

        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._data_path = tools.DataLocation()
        self._hash_utility = tools.FileHash()

    def make_cache(self, data, file_location):
        """
        Makes and hashes the cache with data that was loaded from
        disk.

        Args:
            data (data_types.GenericEvent): Contains the dict of the arrays.
            file_location (str): The location of the original file.

        Raises:
            CacheFailed: Unable to write data to disk.
        """
        try:
            the_pickle = self._data_path.find_cache_dir(file_location,
                                                        '.pickle')
        except definitions.NoCachePath:
            self._logger.info("Failed to find cache.")
            raise CacheFailed("No Cache location found!")

        self._logger.debug("Cache location is set to {0}".format(the_pickle))

        file_hash = self._file_hash(file_location)

        self._logger.info("Found SHA512 hash for {0}".format(file_location))
        self._logger.debug("File Hash is set to {0}".format(file_hash))

        new_data = {"hash": file_hash, "data": data}

        self._logger.info("Making cache for {0}".format(file_location))
        self._write_pickle(the_pickle, new_data)

    def read_cache(self, file_location):
        """
        Parses the cache from the file and checks the cache's hash with
        the hash recovered from the data file.

        Args:
            file_location (str): The location of the original file.

        Returns:
            bool: False if unsuccessful
            dict: Dictionary of Arrays if successful.
        """
        try:
            the_location = self._data_path.find_cache_dir(file_location,
                                                          '.pickle')
        except definitions.NoCachePath:
            self._logger.info("Failed to find cache.")
            raise CacheFailed("No Cache location found!")

        self._logger.debug("Cache location set to {0}".format(the_location))

        file_hash = self._file_hash(file_location)
        self._logger.debug("File hash is set to {0}".format(file_hash))

        self._logger.info("Attempting to load {0}".format(the_location))
        returned_data = self._load_pickle(the_location)

        if returned_data["hash"] == file_hash:
            self._logger.info("Cache Hashes match!")
            return returned_data["data"]
        else:
            self._logger.warning("File hash has changed.")
            self._logger.debug("{0} != {1}".format(
                returned_data["hash"], file_hash))
            return False

    @staticmethod
    def _load_pickle(pickle_location):
        """Loads the cache from file.

        Args:
            pickle_location (str): The location of the cache on disk.

        Returns:
            The contents of the cache, hopefully a dictionary of arrays.
        """
        return pickle.load(io.open(pickle_location, "rb"))

    @staticmethod
    def _write_pickle(pickle_location, data):
        """Writes the data into a cache.

        Args:
            pickle_location (str): The location of the cache.
            data (dict): A dictionary of arrays to be written to disk.
        """
        pickle.dump(data, io.open(pickle_location, "wb"),
                    protocol=pickle.HIGHEST_PROTOCOL)

    def _file_hash(self, file_location):
        with io.open(file_location, "rb") as stream:
            return self._hash_utility.hash_sha512(stream)


class CacheFailed(Exception):
    """
    The Exception for when the Cache Writing has Failed.
    """
    pass
