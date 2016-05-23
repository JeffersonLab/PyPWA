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
Main Objects for the data module.
"""

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.libs.data import data_tools
from PyPWA.libs.data import memory_wrapper
from PyPWA.libs.data import cache

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class MemoryInterface(object):
    def __init__(self, use_cache=False):
        """
        Loads data from disk into memory.

        Args:
            use_cache(optional[bool]): Default is False. Determines if cache
                should be used.
        """
        self.cache = use_cache

    def parse(self, file_location):
        """
        Parses file into memory

        Args:
            file_location (str): The path of the file

        Returns:
            Object: Data that was parsed from the disk.
        """

        if self.cache:
            caching = cache.MemoryCache()
            data = caching.read_cache(file_location)
            if data:
                return data

        tester = data_tools.DataTypeSearch()
        data_type = tester.search(file_location)

        if data_type == "kv":
            reader = memory_wrapper.Kv()
        elif data_type == "sv":
            reader = memory_wrapper.Sv()
        elif data_type == "yaml":
            reader = memory_wrapper.Yaml()
        elif data_type == "pwa":
            reader = memory_wrapper.Binary()
        else:
            raise TypeError("{0} data type is not known!".format(data_type))

        data = reader.parse(file_location)

        if self.cache:
            cache_write = cache.StandardCache()
            cache_write.make_cache(file_location, data)
        return data

    def write(self, file_location, the_data):
        """
        Writes data to disk from memory.

        Args:
            file_location (str): The path to the file.
            the_data (object): The data that needs to be
                written to disk.
        """
        data_type = data_tools.DataTypeWrite.search(file_location)

        if data_type == "sv":
            writer = memory_wrapper.Sv()
        elif data_type == "yaml":
            writer = memory_wrapper.Yaml()
        elif data_type == "pwa":
            writer = memory_wrapper.Binary()
        elif data_type == "kv":
            writer = memory_wrapper.Kv()

        writer.write(file_location, the_data)

        if self.cache:
            cache_write = cache.StandardCache()
            cache_write.make_cache(file_location, the_data)
