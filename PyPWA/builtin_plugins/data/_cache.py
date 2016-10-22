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

"""
Memory Caching

The objects in this file are dedicated to saving and writing chunks of
memory to file for quick loading when the data is loaded into memory
again.
"""

import io
import logging
import os
import pickle

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core import tools

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

        This object caches data stored in the memory on disk in a format
        that can be quickly loaded too and from disk to RAM quickly. Also
        contains logic that will help determine if the the contents of the
        file has changed from the last cache.
        """

        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._hash_utility = tools.FileHash()

    def make_cache(self, data, file_location, cache_path):
        """
        Makes and hashes the cache with data that was loaded from
        disk.

        Args:
            data (data_templates.GenericEvent): Contains the dict of the
                arrays.
            file_location (str): The location of the original file.
            cache_path (str): The path to the cache directory.
        """
        pickle_location = self._determine_cache_location(
            file_location, cache_path
        )

        self._logger.debug(
            "Cache location is set to {0}".format(pickle_location)
        )

        file_hash = self._file_hash(file_location)

        self._logger.info(
            "Found SHA512 hash for {0}".format(file_location)
        )

        self._logger.debug(
            "File Hash is set to {0}".format(file_hash)
        )

        new_data = {"hash": file_hash, "data": data}

        self._logger.info(
            "Making cache for {0}".format(file_location)
        )

        self._write_pickle(pickle_location, new_data)

    def read_cache(self, file_location, cache_path):
        """
        Parses the cache from the file and checks the cache's hash with
        the hash recovered from the data file.

        Args:
            file_location (str): The location of the original file.
            cache_path (str): The path to the cache directory.

        Returns:
            bool: False if unsuccessful
            dict: Dictionary of Arrays if successful.

        Raises:
            CacheError: If the cache is incorrect, doesn't exist, or
                damaged.
        """
        pickle_location = self._determine_cache_location(
            file_location, cache_path
        )

        self._logger.debug(
            "Cache location set to {0}".format(pickle_location)
        )

        file_hash = self._file_hash(file_location)

        self._logger.debug(
            "File hash is set to {0}".format(file_hash)
        )

        self._logger.info(
            "Attempting to load {0}".format(pickle_location)
        )

        try:
            returned_data = self._load_pickle(pickle_location)
        except IOError:
            self._logger.info("No cache exists.")
            raise CacheError()

        if returned_data["hash"] == file_hash:
            self._logger.info("Cache Hashes match!")
            return returned_data["data"]
        else:
            self._logger.warning("File hash has changed.")

            self._logger.debug("{0} != {1}".format(
                returned_data["hash"], file_hash)
            )

            raise CacheError()

    @staticmethod
    def _load_pickle(pickle_location):
        """
        Loads the cache from file.

        Args:
            pickle_location (str): The location of the cache on disk.

        Returns:
            The contents of the cache, hopefully a dictionary of arrays.
        """
        return pickle.load(io.open(pickle_location, "rb"))

    @staticmethod
    def _write_pickle(pickle_location, data):
        """
        Writes the data into a cache.

        Args:
            pickle_location (str): The location of the cache.
            data (dict): A dictionary of arrays to be written to disk.
        """
        pickle.dump(
            data, io.open(pickle_location, "wb"),
            protocol=pickle.HIGHEST_PROTOCOL
        )

    @staticmethod
    def _determine_cache_location(file_location, cache_path):
        """
        Takes the path to the file, extracts the file name, and appends
        it to the cache_path with all needed path extras.

        Args:
            file_location (str): The path to the file that is being
                cached.
            cache_path (str): The path to the cache directory.

        Returns:
            str: The path to the cache file.
        """
        file_name = "." + os.path.basename(file_location).split(".")[0] \
                    + ".pickle"

        path = os.path.abspath(os.path.split(cache_path)[0]) + \
            os.path.sep + file_name

        return path

    def _file_hash(self, file_location):
        with io.open(file_location, "rb") as stream:
            return self._hash_utility.get_sha512_hash(stream)


class CacheError(Exception):
    """
    The Exception for when the Cache Writing or Reading has Failed.
    """
    pass
