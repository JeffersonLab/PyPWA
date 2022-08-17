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
import pandas as pd

from PyPWA import info as _info
from PyPWA.libs import common
from PyPWA.libs.file import cache
from PyPWA.plugins import load, data as data_plugins
from . import templates
from ... import vectors

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


SUPPORTED_DATA = Union[npy.ndarray, vectors.ParticlePool, pd.DataFrame]
INPUT_TYPE = Union[Path, str]


def _get_read_plugin(
        filename: Path, needs_iterator: bool
) -> templates.IDataPlugin:
    found_plugins = load(data_plugins, "Data")
    for plugin in found_plugins:
        if plugin.get_read_test().can_read(filename):
            if not needs_iterator or plugin.supports_iterators:
                return plugin
    raise RuntimeError("Couldn't find plugin for {0}".format(filename))


def _get_write_plugin(
        filename: Path, data_type: templates.DataType, needs_iterator: bool
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
        self.__use_cache = use_cache
        self.__clear_cache = clear_cache

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"({self.__use_cache}, {self.__clear_cache})")

    def parse(
            self, filename: Path, use_pandas: bool
    ) -> Union[pd.DataFrame, pd.Series]:
        valid, cache_obj = cache.read(
            filename, intermediate=False, remove_cache=self.__clear_cache
        )
        if valid and self.__use_cache:
            self.__LOGGER.info("Loading cache for %s" % filename)
            data = cache_obj
        else:
            print("Reading data")
            self.__LOGGER.info("No cache found, loading file directly.")
            data = self.__read_data(filename)

        if use_pandas:
            if data.dtype.names:
                return pd.DataFrame(data)
            return pd.Series(data)
        else:
            return data

    def __read_data(self, filename):
        plugin = _get_read_plugin(filename, False)
        data = plugin.get_memory_parser().parse(filename)
        if self.__use_cache and plugin.use_caching:
            cache.write(filename, data)
        return data


class _DataDumper:

    def __init__(self, use_cache: bool, clear_cache: bool):
        self.__use_cache = use_cache
        self.__clear_cache = clear_cache

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"({self.__use_cache}, {self.__clear_cache})")

    def write(self, filename: Path, data: SUPPORTED_DATA):
        plugin = self.__get_write_plugin(filename, data)
        parser = plugin.get_memory_parser()
        parser.write(filename, data)
        if self.__use_cache and plugin.use_caching:
            if isinstance(data, (pd.DataFrame, pd.Series)):
                data = common.pandas_to_numpy(data)
            cache.write(filename, data, intermediate=False)

    @staticmethod
    def __get_write_plugin(filename: Path,
                           data: SUPPORTED_DATA) -> templates.IDataPlugin:
        if isinstance(data, vectors.ParticlePool):
            data_type = templates.DataType.TREE_VECTOR
        elif isinstance(data, pd.DataFrame):
            data_type = templates.DataType.STRUCTURED
        elif isinstance(data, pd.Series) or not data.dtype.names:
            data_type = templates.DataType.BASIC
        else:
            data_type = templates.DataType.STRUCTURED

        return _get_write_plugin(filename, data_type, False)


class DataProcessor:

    def __init__(self, enable_cache=True, clear_cache=False):
        self.__args = (enable_cache, clear_cache)
        self.__loader = _DataLoader(enable_cache, clear_cache)
        self.__dumper = _DataDumper(enable_cache, clear_cache)

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"({self.__args[0]}, {self.__args[1]})")

    def parse(
            self, filename: INPUT_TYPE, use_pandas: bool = False
    ) -> SUPPORTED_DATA:
        filename = Path(filename)
        return self.__loader.parse(filename, use_pandas)

    @staticmethod
    def get_reader(
            filename: INPUT_TYPE, use_pandas: bool = False
    ) -> templates.ReaderBase:
        filename = Path(filename)
        plugin = _get_read_plugin(filename, True)
        return plugin.get_reader(filename, use_pandas)

    def write(self, filename: INPUT_TYPE, data: SUPPORTED_DATA):
        filename = Path(filename)
        self.__dumper.write(filename, data)

    @staticmethod
    def get_writer(filename: INPUT_TYPE,
                   data_type=templates.DataType.STRUCTURED
                   ) -> templates.WriterBase:
        filename = Path(filename)
        plugin = _get_write_plugin(filename, data_type, True)
        return plugin.get_writer(filename)
