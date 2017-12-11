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

from PyPWA import AUTHOR, VERSION
from PyPWA.libs import configuration_db
from PyPWA.libs.components.data_processor.cache import _basic_info
from PyPWA.libs.components.data_processor.cache import _clear_cache
from PyPWA.libs.components.data_processor.cache import _no_cache
from PyPWA.libs.components.data_processor.cache import _standard_cache
from PyPWA.libs.components.data_processor.cache import _template

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _CacheInterface(object):

    def __init__(self, read_cache, write_cache):
        # type: (_template.ReadInterface, _template.WriteInterface) -> None
        self.__read_cache = read_cache
        self.__write_cache = write_cache

    def write_cache(self, data):
        # type: (Any) -> None
        self.__write_cache.write_cache(data)

    def is_valid(self):
        return self.__read_cache.is_valid()

    def read_cache(self):
        """
        :raises cache.CacheError: If the hash has changed, or is corrupt.
        """
        return self.__read_cache.get_cache()


class CacheBuilder(object):

    __LOGGER = logging.getLogger(__name__ + ".CacheBuilder")

    def __init__(self):
        # type: (bool, bool) -> None
        settings = configuration_db.Connector()
        self.__clear_cache = settings.read("Data Processor", "clear cache")
        self.__use_cache = settings.read("Data Processor", "use cache")
        self.__info_object = None  # type: _basic_info.FindBasicInfo
        self.__selected_reader = None  # type: _template.ReadInterface
        self.__selected_writer = None  # type: _template.WriteInterface

    def get_cache_interface(self, file_location):
        # type: (str) -> _CacheInterface
        self.__set_info_object(file_location)
        self.__find_reader()
        self.__find_writer()
        return self.__make_interface()

    def __set_info_object(self, file_location):
        # type: (str) -> None
        try:
            self.__info_object = _basic_info.FindBasicInfo(file_location)
        except (OSError, IOError):
            self.__LOGGER.warning("No original file found!")
            self.__enable_cache_fallback()

    def __enable_cache_fallback(self):
        self.__LOGGER.debug("Cache set to fallback!")
        self.__use_cache = False

    def __find_reader(self):
        if not self.__use_cache:
            self.__LOGGER.debug("No Read Cache selected.")
            self.__selected_reader = _no_cache.NoRead()
        elif self.__clear_cache:
            self.__LOGGER.debug("Clear Cache selected.")
            self.__selected_reader = _clear_cache.ClearCache(
                self.__info_object
            )
        else:
            self.__LOGGER.debug("Read Cache selected.")
            self.__selected_reader = _standard_cache.ReadCache(
                self.__info_object
            )

    def __find_writer(self):
        if not self.__use_cache:
            self.__LOGGER.debug("No Write Cache selected.")
            self.__selected_writer = _no_cache.NoWrite()
        else:
            self.__LOGGER.debug("Write Cache selected.")
            self.__selected_writer = _standard_cache.WriteCache(
                self.__info_object
            )

    def __make_interface(self):
        # type: () -> _CacheInterface
        return _CacheInterface(
            self.__selected_reader,
            self.__selected_writer
        )
