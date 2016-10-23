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

import hashlib
import io
import logging
import os

class DataLocation(object):

    def __init__(self):
        self._cwd = os.getcwd()
        self._found_uri = None  # type: str

    def get_cache_uri(self, filename: str) -> str: ...

    def get_data_uri(self, filename: str) -> str: ...

    def get_log_uri(self, filename: str) -> str: ...

    def get_config_uri(self, filename: str) -> str: ...

    def _find_usable_uri(self, potential_uri: str) -> str: ...

    @staticmethod
    def _recursively_make_uri_directories(potential_uri: str): ...

    def _determine_potential_or_cwd(self, potential_uri: str): ...

    @staticmethod
    def _check_writable(potential_uri: str): ...

    def _add_filename_to_uri(self, filename: str): ...


class FileHashString(object):

    def __init__(self):
        """
        A simple utility that loads a full stream, hashes it, then returns
        the string of that stream.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        self._stream = None  # type: io.FileIO
        self._hash = None  # type: hashlib.md5
        self._current = 0

    def get_sha512_hash(self, stream: io.FileIO) -> str: ...

    def get_sha384_hash(self, stream: io.FileIO) -> str: ...

    def get_sha256_hash(self, stream: io.FileIO) -> str: ...

    def get_sha224_hash(self, stream: io.FileIO) -> str: ...

    def get_sha1_hash(self, stream: io.FileIO) -> str: ...

    def get_md5_hash(self, stream: io.FileIO) -> str: ...

    def _set_stream(self, stream: io.FileIO): ...

    def _set_hash_type(self, hash_type: hashlib.md5): ...

    def _get_stream_hash(self) -> str: ...

    def _record_stream_cursor_location(self): ...

    def _set_location_to_file_start(self): ...

    def _update_hash(self): ...

    def _set_stream_to_recorded_cursor_position(self): ...

    def _get_string_from_hash(self) -> str: ...
