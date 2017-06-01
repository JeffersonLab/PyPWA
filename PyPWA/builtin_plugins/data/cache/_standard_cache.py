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
Standard Cache
--------------
This simple just writes and reads the cache files without anything special
added to it.

- ReadCache - Loads the cache from disk if it exists, will raise CacheError 
  if something is wrong with the cache.
  
- WriteCache - Writes the cache to disk.
"""

import io
import logging
import pickle
from typing import Any

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import exceptions
from PyPWA.builtin_plugins.data.cache import _basic_info
from PyPWA.builtin_plugins.data.cache import _template

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ReadCache(_template.ReadInterface):

    __LOGGER = logging.getLogger(__name__ + ".ReadCache")

    def __init__(self, basic_info):
        # type: (_basic_info.FindBasicInfo) -> None
        self.__info_object = basic_info
        self.__packaged_data = {"hash": False, "data": object}
        self.__graciously_load_cache()

    def __graciously_load_cache(self):
        self.__LOGGER.debug(
            "Attempting to load %s" % self.__info_object.cache_location
        )

        try:
            self.__load_data()
            self.__LOGGER.debug("Successfully loaded pickle cache!")
        except (OSError, IOError):
            self.__LOGGER.debug("No cache exists.")
        except pickle.PickleError:
            self.__LOGGER.debug("Pickle is from a different python version.")
        except (ValueError, IndexError, KeyError) as error:
            self.__LOGGER.debug("Pickle is damaged.")
            self.__LOGGER.debug(error, exc_info=True)

    def __load_data(self):
        with io.open(self.__info_object.cache_location, "rb") as stream:
            self.__packaged_data = pickle.load(stream)

    def get_cache(self):
        # type: () -> Any
        if self.is_valid():
            return self.__packaged_data["data"]
        else:
            raise exceptions.CacheError

    def is_valid(self):
        # type: () -> bool
        if self.__packaged_data["hash"] == self.__info_object.file_hash:
            self.__LOGGER.debug("Cache Hashes match!")
            return True
        elif not self.__packaged_data["hash"]:
            self.__LOGGER.debug("Cache load failed, hash is false.")
            return False
        else:
            self.__LOGGER.warning("File hash has changed.")
            self.__LOGGER.debug(
                "%s != %s" % (
                    self.__packaged_data["hash"],
                    self.__info_object.file_hash
                )
            )
            return False


class WriteCache(_template.WriteInterface):

    __LOGGER = logging.getLogger(__name__ + ".WriteCache")

    def __init__(self, basic_info):
        # type: (_basic_info.FindBasicInfo) -> None
        self.__info_object = basic_info
        self.__packaged_data = {"hash": False, "data": object}

    def write_cache(self, data):
        # type: (Any) -> None
        self.__set_packaged_data(data)
        self.__write_cache_data()

    def __set_packaged_data(self, data):
        # type: (Any) -> None
        self.__packaged_data["hash"] = self.__info_object.file_hash
        self.__packaged_data["data"] = data

    def __write_cache_data(self):
        location = self.__info_object.cache_location
        self.__LOGGER.debug("Making cache for '%s'" % location)
        with io.open(location, "wb") as stream:
            pickle.dump(
                self.__packaged_data, stream, protocol=pickle.HIGHEST_PROTOCOL
            )
