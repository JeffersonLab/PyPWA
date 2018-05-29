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
from typing import Optional as Opt

import numpy

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs.components.data_processor import (
    _plugin_finder,
    data_templates, exceptions, SUPPORTED_DATA_TYPE
)
from PyPWA.libs.components.data_processor.cache import builder
from PyPWA.libs.math import particle

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _DataLoader(object):

    __LOGGER = logging.getLogger(__name__ + "._DataLoader")

    def __init__(self):
        # type: () -> None
        self.__plugin_search = _plugin_finder.PluginSearch()
        self.__cache_builder = builder.CacheBuilder()
        self.__cache_interface = None  # type: builder._CacheInterface
        self.file_location = None  # type: Path

    def parse(self, file_location):
        # type: (Path) -> numpy.ndarray
        self.file_location = file_location
        self.__set_cache_interface()
        if self.__cache_interface.is_valid():
            self.__LOGGER.info(
                "Found Cache for '%s', loading!" % file_location
            )
            return self.__cache_interface.read_cache()
        else:
            self.__LOGGER.info("No cache found, loading file directly.")
            return self.__parse_with_cache()

    def __set_cache_interface(self):
        self.__cache_interface = self.__cache_builder.get_cache_interface(
            self.file_location
        )

    def __parse_with_cache(self):
        data = self.__read_data()
        self.__cache_interface.write_cache(data)
        return data

    def __read_data(self):
        plugin = self.__load_read_plugin(self.file_location)
        returned_parser = plugin.get_plugin_memory_parser()
        return returned_parser.parse(self.file_location)

    def __load_read_plugin(self, file_location):
        # type: (Path) -> data_templates.DataPlugin
        try:
            return self.__plugin_search.get_read_plugin(file_location)
        except exceptions.UnknownData:
            raise OSError


class _DataDumper(object):

    def __init__(self):
        # type: () -> None
        self.__plugin_search = _plugin_finder.PluginSearch()
        self.__cache_builder = builder.CacheBuilder()
        self.__cache_interface = None  # type: builder._CacheInterface

    def write(self, file_location, data):
        # type: (Path, numpy.ndarray) -> None
        self.__write_data(file_location, data)
        self.__set_cache_interface(file_location)
        self.__cache_interface.write_cache(data)

    def __write_data(self, file_location, data):
        # type: (Path, SUPPORTED_DATA_TYPE) -> None
        plugin = self.__load_write_plugin(file_location, data)
        found_parser = plugin.get_plugin_memory_parser()
        found_parser.write(file_location, data)

    def __set_cache_interface(self, file_location):
        # type: (Path) -> None
        self.__cache_interface = self.__cache_builder.get_cache_interface(
            file_location
        )

    def __load_write_plugin(self, file_location, data):
        # type: (Path, numpy.ndarray) -> data_templates.DataPlugin
        is_pool, is_basic = self.__find_data_type(data)
        try:
            return self.__plugin_search.get_write_plugin(
                file_location, is_pool, is_basic
            )
        except exceptions.UnknownData:
            raise RuntimeError("Can not write data!")

    @staticmethod
    def __find_data_type(data):
        types = [False, False]
        if isinstance(data, particle.ParticlePool):
            types[0] = True
        elif not data.dtype.names:
            types[1] = True
        return types


class _Iterator(object):

    def __init__(self):
        self.__plugin_fetcher = _plugin_finder.PluginSearch()

    def return_reader(self, file_location):
        plugin = self.__plugin_fetcher.get_read_plugin(file_location)
        return plugin.get_plugin_reader(file_location)

    def return_writer(self, file_location, is_particle, is_basic):
        # type: (Path, bool, bool) -> data_templates.Writer
        plugin = self.__plugin_fetcher.get_write_plugin(
            file_location, is_particle, is_basic
        )
        return plugin.get_plugin_writer(file_location)


class DataProcessor(object):

    def __init__(self):
        self.__loader = _DataLoader()
        self.__dumper = _DataDumper()
        self.__iterator = _Iterator()

    def parse(self, file_location):
        # type: (Path) -> numpy.ndarray
        return self.__loader.parse(file_location)

    def fallback_reader(self):
        # type: () -> data_templates.Reader
        return self.__iterator.return_reader(self.__loader.file_location)

    def get_reader(self, file_location):
        # type: (Path) -> data_templates.Reader
        return self.__iterator.return_reader(file_location)

    def write(self, file_location, data):
        # type: (Path, SUPPORTED_DATA_TYPE) -> None
        self.__dumper.write(file_location, data)

    def get_writer(
            self, file_location, is_particle_pool=False, is_basic_type=False
    ):
        # type: (Path, Opt[bool], Opt[bool]) -> data_templates.Writer
        return self.__iterator.return_writer(
            file_location, is_particle_pool, is_basic_type
        )
