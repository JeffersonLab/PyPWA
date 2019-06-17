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
from pathlib import Path
from typing import Union

import numpy as npy

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.file import cache
from PyPWA.libs.math import vectors
from PyPWA.plugins import load, data as data_plugins
from . import templates

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


SUPPORTED_DATA = Union[npy.ndarray, vectors.ParticlePool]


def _get_read_plugin(filename: Path) -> templates.IDataPlugin:
    found_plugins = load(data_plugins, "Data")
    for plugin in found_plugins:
        if plugin.get_read_test().can_read(filename):
            return plugin
    raise RuntimeError("Couldn't find plugin for {0}".format(filename))


def _get_write_plugin(
        filename: Path, data_type: templates.DataType
        ) -> templates.IDataPlugin:
    found_plugins = load(data_plugins, "Data")
    for plugin in found_plugins:
        if data_type in plugin.supported_data_types:
            extension = filename.suffix
            if not extension or extension in plugin.supported_extensions:
                return plugin
    raise RuntimeError("Couldn't find plugin for {0}".format(filename))


class _DataLoader:

    __LOGGER = logging.getLogger(__name__ + "._DataLoader")

    def __init__(self, use_cache: bool, clear_cache: bool):
        self.__args = (use_cache, clear_cache)
        self.__cache_builder = cache.CacheFactory(use_cache, clear_cache)

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"({self.__args[0]}, {self.__args[1]})")

    def parse(self, filename: Path) -> npy.ndarray:
        cache_obj = self.__cache_builder.get_cache(filename)
        if cache_obj.is_valid:
            self.__LOGGER.info("Loading cache for %s" % filename)
            return cache_obj.read_cache()
        else:
            self.__LOGGER.info("No cache found, loading file directly.")
            return self.__read_data(cache_obj, filename)

    @staticmethod
    def __read_data(cache_obj, filename):
        plugin = _get_read_plugin(filename)
        data = plugin.get_memory_parser().parse(filename)
        cache_obj.write_cache(data)
        return data


class _DataDumper:

    def __init__(self, use_cache: bool, clear_cache: bool):
        self.__args = (use_cache, clear_cache)
        self.__cache_builder = cache.CacheFactory(use_cache, clear_cache)

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"({self.__args[0]}, {self.__args[1]})")

    def write(self, filename: Path, data: SUPPORTED_DATA):
        parser = self.__get_write_plugin(filename, data).get_memory_parser()
        cache_obj = self.__cache_builder.get_cache(filename)
        parser.write(filename, data)
        cache_obj.write_cache(data)

    @staticmethod
    def __get_write_plugin(
            filename: Path, data: SUPPORTED_DATA
            )-> templates.IDataPlugin:
        if isinstance(data, vectors.ParticlePool):
            data_type = templates.DataType.TREE_VECTOR
        elif not data.dtype.names:
            data_type = templates.DataType.BASIC
        else:
            data_type = templates.DataType.STRUCTURED

        return _get_write_plugin(filename, data_type)


class DataProcessor:

    def __init__(self, enable_cache=False, clear_cache=False):
        self.__args = (enable_cache, clear_cache)
        self.__loader = _DataLoader(enable_cache, clear_cache)
        self.__dumper = _DataDumper(enable_cache, clear_cache)

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"({self.__args[0]}, {self.__args[1]})")

    def parse(self, filename: Union[Path, str]) -> SUPPORTED_DATA:
        f = filename if isinstance(filename, Path) else Path(filename)
        return self.__loader.parse(f)

    @staticmethod
    def get_reader(filename: Union[Path, str]) -> templates.ReaderBase:
        plugin = _get_read_plugin(Path(filename))
        return plugin.get_reader(Path(filename))

    def write(self, filename: Union[Path, str], data: SUPPORTED_DATA):
        self.__dumper.write(Path(filename), data)

    @staticmethod
    def get_writer(
            filename: Union[Path, str],
            data_type=templates.DataType.STRUCTURED) -> templates.WriterBase:
        plugin = _get_write_plugin(Path(filename), data_type)
        return plugin.get_writer(Path(filename))
