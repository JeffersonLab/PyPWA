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
