__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

class StandardCache(object):
    
    def find_hash(self, the_file):
        """
        Fetches the hash for the data that is to be stored.

        Args: the_file - The file which you wish to find the hash too
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
        """
        Just fetches the location of the cache based off of the location of the original file.

        Params: file_location: the location of the original file.
        """
        the_path = file_location.split("/")
        path_length = len(the_path) - 1
        file_name = the_path[path_length]
        file_name = os.path.splitext(file_name)[0]
        file_name = "." + file_name + ".pickle-cache"
        the_path[path_length] = file_name
        return "/".join(the_path)

        

    def make_cache(self, data, the_file):
        """
        Writes the cache to file.

        Params: the_file: The location where you want the cache to be written.
        """
        with open(the_file, "wb") as a_file:
            pickle.dump(data, a_file, protocol=pickle.HIGHEST_PROTOCOL)


    def load_cache(self, the_file):
        """
        Attempts to load the cache if present.

        Params: the_file: The location of the cache.
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