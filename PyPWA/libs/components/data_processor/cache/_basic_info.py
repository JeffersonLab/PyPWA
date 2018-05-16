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
Finds the hash and cache location for the Cache Module.
"""

import logging
import os

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs import misc_file_libs

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class FindBasicInfo(object):

    __LOGGER = logging.getLogger(__name__ + ".FindBasicInfo")

    def __init__(self, original_file):
        # type: (Path) -> None
        self.__cache_location = None  # type: Path
        self.__found_hash = ""
        self.__setup_basic_info(original_file)

    def __setup_basic_info(self, original_file):
        # type: (Path) -> None
        self.__set_cache_location(original_file)
        self.__set_file_hash(original_file)

    def __set_cache_location(self, original_file):
        # type: (Path) -> None
        cache_location = self.__get_cache_uri()
        location = self.__pair_filename_with_uri(
            original_file, cache_location
        )
        self.__cache_location = location

    def __get_cache_uri(self):
        # type: () -> Path
        potential_cache_location = misc_file_libs.get_cache_uri()
        self.__LOGGER.debug("Found location is %s" % potential_cache_location)
        return potential_cache_location

    def __pair_filename_with_uri(self, original_file, found_location):
        # type: (Path, Path) ->  Path
        final_location = (
            Path(found_location / (original_file.stem + ".pickle"))
        )

        self.__LOGGER.debug("Cache Location set to '%s'" % final_location)
        return final_location

    def __set_file_hash(self, original_file):
        # type: (Path) -> None
        self.__found_hash = self.__file_hash(original_file)
        self.__LOGGER.debug(
            "Found hash '%s' for '%s'" % (
                self.__found_hash, self.__cache_location
            )
        )

    @staticmethod
    def __file_hash(original_file):
        # type: (Path) -> str
        return misc_file_libs.get_sha512_hash(original_file)

    @property
    def file_hash(self):
        return self.__found_hash

    @property
    def cache_location(self):
        return self.__cache_location
