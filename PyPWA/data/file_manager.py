"""
Main Objects for the data module.
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import PyPWA.data.memory_wrapper
import PyPWA.data.data_tools
import PyPWA.data.cache


class MemoryInterface(object):
    """Loads data from disk into memory.
    Args:
        cache(optional[bool]): Default is False. Determines if cache
            should be used.
    """

    def __init__(self, cache=False):
        self.cache = cache

    def parse(self, file_location):
        """Parses file into memory
        Args:
            file_location (str): The path of the file
        Returns:
            Object: Data that was parsed from the disk.
        """

        if self.cache:
            caching = PyPWA.data.cache.StandardCache()
            data = caching.check_cache(file_location)
            if data:
                return data

        tester = PyPWA.data.data_tools.DataTypeSearch()
        data_type = tester.search(file_location)

        if data_type == "kv":
            reader = PyPWA.data.memory_wrapper.Kv()
        elif data_type == "sv":
            reader = PyPWA.data.memory_wrapper.Sv()
        elif data_type == "yaml":
            reader = PyPWA.data.memory_wrapper.Yaml()
        elif data_type == "pwa":
            reader = PyPWA.data.memory_wrapper.Binary()
        else:
            raise TypeError("{0} data type is not known!".format(data_type))

        data = reader.parse(file_location)

        if self.cache:
            cache_write = PyPWA.data.cache.StandardCache()
            cache_write.make_cache(file_location, data)
        return data

    def write(self, file_location, the_data):
        """Writes data to disk from memory.
        Args:
            file_location (str): The path to the file.
            the_data (object): The data that needs to be
                written to disk.
        """
        data_type = PyPWA.data.data_tools.DataTypeWrite.search(file_location)

        if data_type == "sv":
            writer = PyPWA.data.memory_wrapper.Sv()
        elif data_type == "yaml":
            writer = PyPWA.data.memory_wrapper.Yaml()
        elif data_type == "pwa":
            writer = PyPWA.data.memory_wrapper.Binary()
        elif data_type == "kv":
            writer = PyPWA.data.memory_wrapper.Kv()

        writer.write(file_location, the_data)

        if self.cache:
            cache_write = PyPWA.data.cache.StandardCache()
            cache_write.make_cache(file_location, the_data)

