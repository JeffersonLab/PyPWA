"""
Cache objects for data module are stored here.
"""
import pickle
import io
import hashlib
import os
import appdirs
import logging

__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"


class MemoryCache(object):
    """Just like the old one, but new!"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())

    def make_cache(self, data, file_location, pickle_location=False):
        the_pickle = pickle_location or self._find_location(file_location)
        self.logger.debug("Cache location is set to {0}".format(the_pickle))

        file_hash = self._file_hash(file_location)
        self.logger.debug("File Hash is set to {0}".format(file_hash))

        new_data = {"hash": file_hash, "data": data}

        try:
            self._write_pickle(the_pickle, new_data)
        except Exception as Error:
            self.logger.warning(Error)
            self.logger.warning("Falling back onto alternative location.")
            try:
                the_pickle = self._find_location(file_location, fallback=True)
                self.logger.debug("New Cache location set to {0}".format(the_pickle))
                self._write_pickle(the_pickle, new_data)
            except Exception as Error:
                self.logger.error(Error)
                raise CacheFailed("Failed to write cache!")

    def read_cache(self, file_location, pickle_location=False):
        the_location = pickle_location or self._find_location(file_location)
        self.logger.debug("Cache location set to {0}".format(the_location))

        file_hash = self._file_hash(file_location)
        self.logger.debug("File hash is set to {0}".format(file_hash))

        try:
            returned_data = self._load_pickle(the_location)
        except Exception as Error:
            self.logger.warning(Error)
            self.logger.warning("Falling back onto alternative location")
            try:
                the_location = self._find_location(file_location, fallback=True)
                self.logger.debug("New Cache location set to {0}".format(the_location))
                returned_data = self._load_pickle(the_location)
            except Exception as Error:
                self.logger.warning(Error)
                return False

        if returned_data["hash"] == file_hash:
            return returned_data["data"]
        else:
            self.logger.warning("File hash has changed.")
            self.logger.debug("{0} != {1}".format(returned_data["hash"], file_hash))
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
        the_hash = hashlib.sha512()
        with io.open(the_file, "rb") as stream:
            for chunk in iter(lambda: stream.read(4096), b""):
                the_hash.update(chunk)
        return the_hash.hexdigest()

    @staticmethod
    def _load_pickle(pickle_location):
        return pickle.load(io.open(pickle_location, "rb"))

    @staticmethod
    def _write_pickle(pickle_location, data):
        pickle.dump(data, io.open(pickle_location, "wb"), protocol=pickle.HIGHEST_PROTOCOL)


class CacheFailed(Exception):
    pass


class NoCachePath(Exception):
    pass
