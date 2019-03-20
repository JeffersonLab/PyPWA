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
Memory Caching
--------------
The objects in this file are dedicated to saving and writing chunks of
memory to file for quick loading when the data is loaded into memory
again.

- _CacheInterface - A simple interface object to _WriteCache and _ReadCache

- CacheBuilder - Builds the _CacheInterface using the other cache types
  depending on the supplied booleans.
"""

import logging
from typing import Any

from PyPWA import Path, AUTHOR, VERSION
from . import _basic_info, _clear_cache, _no_cache, _standard_cache, _template

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _CacheInterface:

    def __init__(
            self, read_cache: _template.ReadInterface,
            write_cache: _template.WriteInterface):
        self.__read_cache = read_cache
        self.__write_cache = write_cache

    def __repr__(self) -> str:
        return "{0}({1}, {2})".format(
            self.__class__.__name__, self.__read_cache, self.__write_cache
        )

    def write_cache(self, data: Any):
        self.__write_cache.write_cache(data)

    def is_valid(self) -> bool:
        return self.__read_cache.is_valid()

    def read_cache(self) -> Any:
        """
        :raises cache.CacheError: If the hash has changed, or is corrupt.
        """
        return self.__read_cache.get_cache()


class CacheBuilder:

    __LOGGER = logging.getLogger(__name__ + ".CacheBuilder")

    def __init__(self, use_cache: bool, clear_cache: bool):
        self.__use_cache = use_cache
        self.__clear_cache = clear_cache

    def __repr__(self) -> str:
        return "{0}({1}, {2})".format(
            self.__class__.__name__, self.__use_cache, self.__clear_cache
        )

    def get_cache_interface(self, file_location: Path) -> _CacheInterface:
        info_object = self.__get_info_object(file_location)
        reader = self.__get_reader(info_object)
        writer = self.__get_writer(info_object)
        return _CacheInterface(reader, writer)

    @staticmethod
    def __get_info_object(file_location: Path) -> _basic_info.FindBasicInfo:
        info = _basic_info.FindBasicInfo()
        info.setup_basic_info(file_location)
        return info

    def __get_reader(
            self, info: _basic_info.FindBasicInfo) -> _template.ReadInterface:
        if not self.__use_cache or not info.file_hash:
            self.__LOGGER.debug("No Read Cache selected.")
            return _no_cache.NoRead()
        elif self.__clear_cache:
            self.__LOGGER.debug("Clear Cache selected.")
            return _clear_cache.ClearCache(info)
        else:
            self.__LOGGER.debug("Read Cache selected.")
            return _standard_cache.ReadCache(info)

    def __get_writer(
            self, info: _basic_info.FindBasicInfo) -> _template.WriteInterface:
        if not self.__use_cache:
            self.__LOGGER.debug("No Write Cache selected.")
            return _no_cache.NoWrite()
        else:
            self.__LOGGER.debug("Write Cache selected.")
            return _standard_cache.WriteCache(info)
