#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

"""

import abc
import logging
import os

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core.shared import data_locator
from PyPWA.core.shared import generate_hash

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class BasicInfoInterface(object):
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def file_hash(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def cache_location(self):
        raise NotImplementedError


class FindBasicInfo(BasicInfoInterface):
    _logger = logging.getLogger(__name__)
    _cache_location = ""
    _found_hash = ""

    def __init__(self, original_file):
        """
        Finds the hash and cache location for the Cache Module.
        """
        self._setup_basic_info(original_file)
        self._logger.addHandler(logging.NullHandler())

    @property
    def file_hash(self):
        return self._found_hash

    @property
    def cache_location(self):
        return self._cache_location

    def _setup_basic_info(self, original_file):
        self._set_cache_location(original_file)
        self._set_file_hash(original_file)

    def _set_cache_location(self, original_file):
        cache_location = self._get_cache_uri()
        location = self._pair_filename_with_uri(original_file, cache_location)
        self._cache_location = location

    def _get_cache_uri(self):
        potential_cache_location = data_locator.get_cache_uri()
        self._logger.debug("Found location is %s" % potential_cache_location)
        return potential_cache_location

    def _pair_filename_with_uri(self, original_file, found_location):
        beginning_of_uri = "/"
        filename_extension = ".pickle"

        filename_base = os.path.basename(original_file)
        filename_without_extension = filename_base.split(".")[0]

        final_location = (
            found_location + beginning_of_uri +
            filename_without_extension + filename_extension
        )

        self._logger.info("Cache Location set to %s" % final_location)
        return final_location

    def _set_file_hash(self, original_file):
        self._found_hash = self._file_hash(original_file)

        self._logger.info("Found SHA512 hash for %s" % self._cache_location)
        self._logger.debug("File Hash is set to %s" % self._found_hash)

    def _file_hash(self, original_file):
        return generate_hash.get_sha512_hash(original_file)
