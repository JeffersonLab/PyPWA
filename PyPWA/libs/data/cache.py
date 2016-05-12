# The MIT License (MIT)
#
# Copyright (c) 2014-2016 JLab.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Memory Caching

The objects in this file are dedicated to saving and writing chunks of memory
to file for quick loading when the data is loaded into memory again.
"""

import hashlib
import io
import logging
import os
import pickle

import appdirs

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

        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

    def make_cache(self, data, file_location, pickle_location=False):
        """
        Makes and hashes the cache with data that was loaded from
        disk.

        Args:
            data (dict): Contains the dict of the arrays.
            file_location (str): The location of the original file.
            pickle_location (Optional[str]): Where to write the cache.

        Raises:
            CacheFailed: Unable to write data to disk.
        """
        the_pickle = pickle_location or self._find_location(file_location)
        self.logger.debug("Cache location is set to {0}".format(the_pickle))

        file_hash = self._file_hash(file_location)
        self.logger.info("Found SHA512 hash for {0}".format(file_location))
        self.logger.debug("File Hash is set to {0}".format(file_hash))

        new_data = {"hash": file_hash, "data": data}

        try:
            self.logger.info("Attempting to make cache for "
                             "{0}".format(file_location))
            self._write_pickle(the_pickle, new_data)
        except Exception as Error:
            self.logger.warning(Error)
            self.logger.warning("Falling back onto alternative location.")
            try:
                the_pickle = self._find_location(file_location, fallback=True)
                self.logger.debug("New Cache location set to "
                                  "{0}".format(the_pickle))
                self._write_pickle(the_pickle, new_data)
            except Exception as Error:
                self.logger.error(Error)
                raise CacheFailed("Failed to write cache!")

    def read_cache(self, file_location, pickle_location=False):
        """
        Parses the cache from the file and checks the cache's hash with
        the hash recovered from the data file.

        Args:
            file_location (str): The location of the original file.
            pickle_location (Optional[str]): The location of the cache.

        Returns:
            bool: False if unsuccessful
            dict: Dictionary of Arrays if successful.
        """
        the_location = pickle_location or self._find_location(file_location)
        self.logger.debug("Cache location set to {0}".format(the_location))

        file_hash = self._file_hash(file_location)
        self.logger.debug("File hash is set to {0}".format(file_hash))

        try:
            self.logger.info("Attempting to load {0}".format(the_location))
            returned_data = self._load_pickle(the_location)
        except Exception as Error:
            self.logger.warning(Error)
            self.logger.warning("Falling back onto alternative location")
            try:
                the_location = self._find_location(file_location, fallback=True)
                self.logger.debug("New Cache location set to "
                                  "{0}".format(the_location))
                returned_data = self._load_pickle(the_location)
            except Exception as Error:
                self.logger.warning(Error)
                return False

        if returned_data["hash"] == file_hash:
            self.logger.info("Cache Hashes match!")
            return returned_data["data"]
        else:
            self.logger.warning("File hash has changed.")
            self.logger.debug("{0} != {1}".format(returned_data["hash"],
                                                  file_hash))
            return False

    @staticmethod
    def _find_location(file_location, fallback=False):
        """
        Searches for the location of the cache, will first return the location
        of theOSes user cache location, then will return the location of the
        data with caches.

        Args:
            file_location (str): The location of the data.
            fallback (bool): True to put the method into fallback to return the
                data location, false to us OS location.

        Returns:
            str: The location of the cache.
        """
        file_name = os.path.splitext(os.path.basename(file_location
                                                      ))[0] + ".pickle"
        if os.path.exists(appdirs.user_cache_dir()) and not fallback:
            if not os.path.exists(appdirs.user_cache_dir("PyPWA", "Jlab")):
                os.makedirs(appdirs.user_cache_dir("PyPWA", "Jlab"))
            return appdirs.user_cache_dir("PyPWA", "Jlab"
                                          ) + os.path.sep + file_name
        else:
            return os.path.dirname(file_location) + os.path.sep + file_name

    @staticmethod
    def _file_hash(the_file):
        """Finds the hash of the file.
        Loads the contents of the file to create a SHA512 sum of the file.

        Args:
            the_file (str): Location of the data file.

        Returns:
            str: The SHA512 sum of the file.
        """
        the_hash = hashlib.sha512()
        with io.open(the_file, "rb") as stream:
            for chunk in iter(lambda: stream.read(4096), b""):
                the_hash.update(chunk)
        return the_hash.hexdigest()

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


class CacheFailed(Exception):
    """
    The Exception for when the Cache Writing has Failed.
    """
    pass


class NoCachePath(Exception):
    """
    The Exception for when the object was unable to determine a writable path
    for the cache.
    """
    pass
