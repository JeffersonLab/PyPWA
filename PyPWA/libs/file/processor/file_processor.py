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
from typing import Union

import numpy

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs.file.cache import builder
from PyPWA.libs.math import vectors
from . import _plugin_finder
from . import data_templates

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


SUPPORTED_DATA = Union[numpy.ndarray, vectors.ParticlePool]


class _DataLoader(object):

    __LOGGER = logging.getLogger(__name__ + "._DataLoader")

    def __init__(self, use_cache, clear_cache):
        # type: (bool, bool) -> None
        self.__args = (use_cache, clear_cache)
        self.__plugin_search = _plugin_finder.PluginSearch()
        self.__cache_builder = builder.CacheBuilder(use_cache, clear_cache)

    def __repr__(self):
        return "{0}({1}, {2})".format(
            self.__class__.__name__, self.__args[0], self.__args[1]
        )

    def parse(self, filename, precision):
        # type: (Path, numpy.floating) -> numpy.ndarray
        cache = self.__cache_builder.get_cache_interface(filename)
        if cache.is_valid():
            self.__LOGGER.info("Loading cache for %s" % filename)
            return cache.read_cache()
        else:
            self.__LOGGER.info("No cache found, loading file directly.")
            return self.__read_data(cache, filename, precision)

    def __read_data(self, cache, filename, precision):
        plugin = self.__plugin_search.get_read_plugin(filename)
        data = plugin.get_memory_parser().parse(filename, precision)
        cache.write_cache(data)
        return data


class _DataDumper(object):

    def __init__(self, use_cache, clear_cache):
        # type: (bool, bool) -> None
        self.__args = (use_cache, clear_cache)
        self.__plugin_search = _plugin_finder.PluginSearch()
        self.__cache_builder = builder.CacheBuilder(use_cache, clear_cache)

    def __repr__(self):
        return "{0}({1}, {2})".format(
            self.__class__.__name__, self.__args[0], self.__args[1]
        )

    def write(self, filename, data):
        # type: (Path, SUPPORTED_DATA) -> None
        parser = self.__get_write_plugin(filename, data).get_memory_parser()
        cache = self.__cache_builder.get_cache_interface(filename)
        parser.write(filename, data)
        cache.write_cache(data)

    def __get_write_plugin(self, filename, data):
        # type: (Path, SUPPORTED_DATA) -> data_templates.DataPlugin
        if isinstance(data, vectors.ParticlePool):
            data_type = data_templates.DataType.TREE_VECTOR
        elif not data.dtype.names:
            data_type = data_templates.DataType.BASIC
        else:
            data_type = data_templates.DataType.STRUCTURED

        return self.__plugin_search.get_write_plugin(filename, data_type)


class _Iterator(object):

    def __init__(self):
        self.__plugin_fetcher = _plugin_finder.PluginSearch()

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

    def return_reader(self, filename, precision):
        # type: (Path, numpy.floating) -> data_templates.Reader
        plugin = self.__plugin_fetcher.get_read_plugin(filename)
        return plugin.get_reader(filename, precision)

    def return_writer(self, filename, data_type):
        # type: (Path, data_templates.DataType) -> data_templates.Writer
        plugin = self.__plugin_fetcher.get_write_plugin(filename, data_type)
        return plugin.get_writer(filename)


class DataProcessor(object):

    def __init__(self, enable_cache=False, clear_cache=False):
        self.__args = (enable_cache, clear_cache)
        self.__loader = _DataLoader(enable_cache, clear_cache)
        self.__dumper = _DataDumper(enable_cache, clear_cache)
        self.__iterator = _Iterator()

    def __repr__(self):
        return "{0}({1}, {2})".format(
            self.__class__.__name__, self.__args[0], self.__args[1]
        )

    def parse(self, filename, precision=numpy.float64):
        # type: (Path, numpy.floating) -> SUPPORTED_DATA
        return self.__loader.parse(filename, precision)

    def get_reader(self, filename, precision=numpy.float64):
        # type: (Path, numpy.floating) -> data_templates.Reader
        return self.__iterator.return_reader(filename, precision)

    def write(self, filename, data):
        # type: (Path, SUPPORTED_DATA) -> None
        self.__dumper.write(filename, data)

    def get_writer(
            self, filename, data_type=data_templates.DataType.STRUCTURED
    ):
        # type: (Path, data_templates.DataType) -> data_templates.Writer
        return self.__iterator.return_writer(filename, data_type)
