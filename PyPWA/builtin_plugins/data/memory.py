#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016 JLab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Main object for Parsing Data
"""

import logging

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import _plugin_finder
from PyPWA.builtin_plugins.data import exceptions
from PyPWA.builtin_plugins.data.cache import builder
from PyPWA.core.shared.interfaces import plugins
from PyPWA.builtin_plugins.data import data_templates

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Memory(plugins.DataParser):

    __LOGGER = logging.getLogger(__name__ + ".Memory")

    def __init__(
            self, enable_cache=True, clear_cache=False,
            user_plugin_dir=""
    ):
        # type: (bool, bool, str) -> None
        self.__plugin_search = _plugin_finder.PluginSearch(user_plugin_dir)
        self.__cache_builder = builder.CacheBuilder(enable_cache, clear_cache)
        self.__cache_interface = None  # type: builder._CacheInterface

    def parse(self, file_location):
        # type: (str) -> numpy.ndarray
        self.__set_cache_interface(file_location)
        if self.__cache_interface.is_valid():
            self.__LOGGER.info(
                "Found Cache for '%s', loading!" % file_location
            )
            return self.__cache_interface.read_cache()
        else:
            self.__LOGGER.info("No cache found, loading file directly.")
            return self.__parse_with_cache(file_location)

    def __set_cache_interface(self, file_location):
        # type: (str) -> None
        self.__cache_interface = self.__cache_builder.get_cache_interface(
            file_location
        )

    def __parse_with_cache(self, file_location):
        # type: (str) -> numpy.ndarray
        data = self.__read_data(file_location)
        self.__cache_interface.write_cache(data)
        return data

    def __read_data(self, file_location):
        # type: (str) -> numpy.ndarray
        plugin = self.__load_read_plugin(file_location)
        returned_parser = plugin.get_plugin_memory_parser()
        return returned_parser.parse(file_location)

    def __load_read_plugin(self, file_location):
        # type: (str) -> data_templates.TemplateDataPlugin
        try:
            return self.__plugin_search.get_read_plugin(file_location)
        except exceptions.UnknownData:
            raise OSError

    def write(self, file_location, data):
        # type: (str, numpy.ndarray) -> None
        self.__write_data(file_location, data)
        self.__set_cache_interface(file_location)
        self.__cache_interface.write_cache(data)

    def __write_data(self, file_location, data):
        # type: (str, numpy.ndarray) -> None
        plugin = self.__load_write_plugin(file_location, data)
        found_parser = plugin.get_plugin_memory_parser()
        found_parser.write(file_location, data)

    def __load_write_plugin(self, file_location, data):
        # type: (str, numpy.ndarray) -> data_templates.TemplateDataPlugin
        try:
            return self.__plugin_search.get_write_plugin(file_location, data)
        except exceptions.UnknownData:
            raise RuntimeError
