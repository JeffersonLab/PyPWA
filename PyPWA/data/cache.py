"""
Cache objects for data module are stored here.
"""
from abc import ABCMeta
import pickle
import fileinput
import hashlib
import os
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"


class AbstractCache:
    __metaclass__ = ABCMeta

    @staticmethod
    def find_hash(the_file):
        """ Iterates over file and returns the hash
        Args:
            the_file (str): the file you want to be loaded.
        Returns:
            str: sha256 hash of file
        """
        for line in fileinput.input(the_file):
            the_hash = hashlib.sha256(line.strip("\n"))

        return the_hash.hexdigest()


class StandardCache(AbstractCache):

    def check_cache(self, file_location):
        path_cache = self._cache_location(file_location)

        try:
            data = self._load_cache(path_cache)
        except:
            return False

        file_hash = self.find_hash(file_location)

        if data["hash"] == file_hash:
            return data["data"]
        else:
            return False

    def make_cache(self, file_location, data):
        path_cache = self._cache_location(file_location)
        file_hash = self.find_hash(file_location)

        cache = {"data": data, "hash": file_hash}

        self._write_cache(path_cache, cache)

    @staticmethod
    def _cache_location(file_location):
        """ Determines where to store cache
        Args:
            file_location (str): the location of the original file.
        Returns:
            str: Absolute location of where to store the cache
        """
        file_name = os.path.splitext(os.path.basename(file_location))[0]
        pickle_name = "." + file_name + ".pickle-cache"
        return pickle_name

    @staticmethod
    def _write_cache(the_file, data):
        """Pickles the data to file.
        Args:
            data: Anything that needs to be cached
            the_file (str): Where to write the cache
        """
        with open(the_file, "wb") as a_file:
            pickle.dump(data, a_file, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def _load_cache(the_file):
        """Attempts to load the cache from file,
        Args:
            the_file (str): location of the cache
        Returns:
            dict: {"hash": hash of file, "data": data that was cached}
        """
        with open(the_file, "r") as stream:
            cache = pickle.load(stream)
        return cache
