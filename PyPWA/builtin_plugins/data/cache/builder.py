#   PyPWA, a scientific analysis toolkit.
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
Memory Caching

The objects in this file are dedicated to saving and writing chunks of
memory to file for quick loading when the data is loaded into memory
again.
"""

import logging

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.builtin_plugins.data.cache import _basic_info
from PyPWA.builtin_plugins.data.cache import _clear_cache
from PyPWA.builtin_plugins.data.cache import _no_cache
from PyPWA.builtin_plugins.data.cache import _standard_cache
from PyPWA.builtin_plugins.data.cache import _template

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _CacheInterface(object):

    _read_cache = _template.ReadInterface
    _write_cache = _template.WriteInterface

    def __init__(self, read_cache, write_cache):
        """
        A simple interface object to _WriteCache and _ReadCache.
        """
        self._read_cache = read_cache
        self._write_cache = write_cache

    def write_cache(self, data):
        self._write_cache.write_cache(data)

    @property
    def is_valid(self):
        return self._read_cache.is_valid

    def read_cache(self):
        """
        Raises:
            cache.CacheError: If the hash has changed, is corrupt, or
                doesn't exist, this error will be raised.
        """
        return self._read_cache.get_cache()


class CacheBuilder(object):
    _use_cache = True
    _clear_cache = False
    _info_object = _basic_info.FindBasicInfo
    _selected_reader = _template.ReadInterface
    _selected_writer = _template.WriteInterface
    _logger = logging.getLogger(__name__)

    def __init__(self, use_cache=True, clear_cache=False):
        self._logger.addHandler(logging.NullHandler())
        self._clear_cache = clear_cache
        self._use_cache = use_cache

    def get_cache_interface(self, file_location):
        self._set_info_object(file_location)
        self._find_reader()
        self._find_writer()
        return self._make_interface()

    def _set_info_object(self, file_location):
        try:
            self._info_object = _basic_info.FindBasicInfo(file_location)
        except (OSError, IOError):
            self._logger.warning("No original file found!")
            self._enable_cache_fallback()

    def _enable_cache_fallback(self):
        self._logger.debug("Cache set to fallback!")
        self._use_cache = False

    def _find_reader(self):
        if not self._use_cache:
            self._logger.debug("No Read Cache selected.")
            self._selected_reader = _no_cache.NoRead()
        elif self._clear_cache:
            self._logger.debug("Clear Cache selected.")
            self._selected_reader = _clear_cache.ClearCache(self._info_object)
        else:
            self._logger.debug("Read Cache selected.")
            self._selected_reader = _standard_cache.ReadCache(
                self._info_object
            )

    def _find_writer(self):
        if not self._use_cache:
            self._logger.debug("No Write Cache selected.")
            self._selected_writer = _no_cache.NoWrite()
        else:
            self._logger.debug("Write Cache selected.")
            self._selected_writer = _standard_cache.WriteCache(
                self._info_object
            )

    def _make_interface(self):
        return _CacheInterface(
            self._selected_reader,
            self._selected_writer
        )
