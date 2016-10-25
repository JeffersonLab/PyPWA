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

import logging

import numpy

from PyPWA.core import tools


class MemoryCache(object):

    @staticmethod
    def write_cache(data: numpy.ndarray, file_location: str): ...

    @staticmethod
    def read_cache(file_location: str) -> numpy.ndarray: ...

    def delete_cache(self, file_location: str): ...

    @staticmethod
    def _attempt_to_delete_cache(basic_data: _FindBasicInfo): ...


class _FindBasicInfo(object):

    _logger = logging.getLogger(__name__)
    _hash_utility = tools.FileHashString()
    _data_locator = tools.DataLocation()
    _cache_location = ""
    _found_hash = ""

    def __init__(self, original_file: str): ...

    @property
    def file_hash(self) -> str: ...

    @property
    def cache_location(self) -> str: ...

    def _setup_basic_info(self, file_location: str): ...

    def _set_cache_location(self, file_location) -> str: ...

    def _get_cache_uri(self) -> str: ...

    def _pair_filename_with_uri(self, file_location: str, found_location: str) -> str: ...

    def _set_file_hash(self, file_location: str): ...

    def _file_hash(self, file_location: str) -> str: ...


class _ReadCache(object):

    _info_object = _FindBasicInfo
    _packaged_data = {"hash": "", "data": object}
    _logger = logging.getLogger(__name__)

    def __init__(self, basic_info: _FindBasicInfo): ...

    def read_cache(self) -> numpy.ndarray: ...

    def _attempt_cache_load(self): ...

    def _graciously_load_cache(self) -> dict: ...

    @property
    def _empty_raw_data(self) -> str: ...

    def _load_data(self) -> dict: ...

    def _if_valid_set_data(self, loaded_data: dict): ...

    def _check_cache_is_valid(self, loaded_data: dict) -> bool: ...

    def _caches_match(self) -> bool: ...

    def _cache_hash_is_false(self) -> bool: ...

    def _cache_hash_changed(self, loaded_data: dict) -> bool: ...


class _WriteCache(object):

    _packaged_data = {"hash": "", "data": object}
    _logger = logging.getLogger(__name__)
    _info_object = _FindBasicInfo

    def __init__(self, basic_info: _FindBasicInfo): ...

    def write_cache(self, data: numpy.ndarray): ...

    def _set_packaged_data(self, data): ...

    def _write_cache_data(self): ...
