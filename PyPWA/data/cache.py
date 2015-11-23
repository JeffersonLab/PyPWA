"""
Cache objects for data module are stored here.
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import pickle, hashlib, os

class StandardCache(object):
    """
    This is a horribly written object, please ignore. It currently is unimplemented.

    Todo:
        Write a propper init, imply
    """

    def __init__(self):
        raise NotImplemented


    def find_hash(self, the_file):
        """ Iterates over file and returns the hash
        Args:
            the_file (str): the file you want to be loaded.
        Returns:
            str: sha256 hash of file
        """
        try:
            with open(the_file, "r") as a_file:
                for line in a_file.readlines():
                    line = line.strip("\n")
                    the_hash = hashlib.sha256(line)
        except IOError:
            raise AttributeError(the_file + " doesn't exsist. Please check your configuration and try again.")
        return the_hash.hexdigest()


    def cache_location(self, file_location):
        """ Determines where to store cache
        Args:
            file_location (str): the location of the original file.
        Returns:
            str: Absolute location of where to store the cache
        """
        the_path = file_location.split("/")
        path_length = len(the_path) - 1
        file_name = the_path[path_length]
        file_name = os.path.splitext(file_name)[0]
        file_name = "." + file_name + ".pickle-cache"
        the_path[path_length] = file_name
        return "/".join(the_path)


    def make_cache(self, data, the_file):
        """Pickles the data to file.
        Args:
            data: Anything that needs to be cached
            the_file (str): Where to write the cache
        """
        with open(the_file, "wb") as a_file:
            pickle.dump(data, a_file, protocol=pickle.HIGHEST_PROTOCOL)


    def load_cache(self, the_file):
        """Attempts to load the cache from file,
        Args:
            the_file (str): location of the cache
        Returns:
            object: Whatever was stored in the cache
        """
        try:
            with open(the_file, "r")  as a_file:
                cache = pickle.load(a_file)
            self.cache_success = True
            return cache
        except EOFError:
            self.cache_success = False
            return {"files_hash":0}
        except IOError:
            self.cache_success = False
            return {"files_hash":0}
