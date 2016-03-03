"""
Cache objects for data module are stored here.
"""
import pickle
import fileinput
import hashlib
import os
import appdirs
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"


class MemoryCache(object):
    """Just like the old one, but new!"""

    def make_cache(self, data, file_location, pickle_location=False):
        the_pickle = pickle_location or self._find_location(file_location)
        file_hash = self._file_hash(file_location)
        new_data = {"hash": file_hash, "data": data}

        try:
            self._write_pickle(the_pickle, new_data)
        except:
            try:
                the_pickle = self._find_location(file_location, fallback=True)
                self._write_pickle(the_pickle, new_data)
            except:
                raise CacheFailed("Failed to write cache!")

    def read_cache(self, file_location, pickle_location=False):
        the_location = pickle_location or self._find_location(file_location)
        file_hash = self._file_hash(file_location)

        try:
            returned_data = self._load_pickle(the_location)
        except:
            try:
                the_location = self._find_location(file_location, fallback=True)
                returned_data = self._load_pickle(the_location)
            except:
                return False

        if returned_data["hash"] == file_hash:
            return returned_data["data"]
        else:
            return False

    @staticmethod
    def _find_location(file_location, fallback=False):
        file_name = "." + os.path.splitext(os.path.basename(file_location))[0] + ".pickle"
        if os.path.exists(appdirs.user_cache_dir()) and not fallback:
            if not os.path.exists(appdirs.user_cache_dir("PyPWA", "Jlab")):
                os.makedirs(appdirs.user_cache_dir("PyPWA", "Jlab"))
            return appdirs.user_cache_dir("PyPWA", "Jlab") + os.path.sep + file_name
        else:
            return os.path.dirname(file_location) + os.path.sep + file_name

    @staticmethod
    def _file_hash(the_file):
        the_hash = ""
        with fileinput.input(the_file) as stream:
            for line in stream:
                the_hash = hashlib.sha256(line.strip("\n").encode("utf-8"))
        return the_hash

    @staticmethod
    def _load_pickle(pickle_location):
        return pickle.load(open(pickle_location, "rb"))

    @staticmethod
    def _write_pickle(pickle_location, data):
        pickle.dump(data, open(pickle_location, "wb"), protocol=pickle.HIGHEST_PROTOCOL)


class CacheFailed(Exception):
    pass


class NoCachePath(Exception):
    pass
