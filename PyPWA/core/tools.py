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

import hashlib
import io
import logging
import os

import appdirs
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class DataLocation(object):

    def __init__(self):
        """
        Locates a place to store cache, logs, configuration, and data.
        """
        self._cwd = os.getcwd()
        self._found_uri = None

    def get_cache_uri(self, filename):
        possible_uri = appdirs.user_cache_dir("PyPWA", "JLab", __version__)
        self._find_usable_uri(possible_uri)
        self._add_filename_to_uri(filename)
        return self._found_uri

    def get_data_uri(self, filename):
        possible_uri = appdirs.user_data_dir("PyPWA", "JLab", __version__)
        self._find_usable_uri(possible_uri)
        self._add_filename_to_uri(filename)
        return self._found_uri

    def get_log_uri(self, filename):
        possible_uri = appdirs.user_log_dir("PyPWA", "JLab", __version__)
        self._find_usable_uri(possible_uri)
        self._add_filename_to_uri(filename)
        return self._found_uri

    def get_config_uri(self, filename):
        possible_uri = appdirs.user_config_dir("PyPWA", "JLab", __version__)
        self._find_usable_uri(possible_uri)
        self._add_filename_to_uri(filename)
        return self._found_uri

    def _find_usable_uri(self, potential_uri):
        self._recursively_make_uri_directories(potential_uri)
        self._determine_potential_or_cwd(potential_uri)

    @staticmethod
    def _recursively_make_uri_directories(potential_uri):
        try:
            os.makedirs(potential_uri)
        except OSError:
            pass

    def _determine_potential_or_cwd(self, potential_uri):
        try:
            self._check_writable(potential_uri)
            self._found_uri = potential_uri
        except OSError:
            self._check_writable(self._cwd)
            self._found_uri = self._cwd

    @staticmethod
    def _check_writable(potential_uri):
        test_file = potential_uri + "/test"
        with open(test_file, "w") as stream:
            stream.write("test")
        os.remove(test_file)

    def _add_filename_to_uri(self, filename):
        self._found_uri += "/" + filename


class FileHashString(object):

    def __init__(self):
        """
        A simple utility that takes an io stream and returns its hash
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        self._stream = None
        self._hash = None
        self._current = 0

    def get_sha512_hash(self, stream):
        self._set_stream(stream)
        self._set_hash_type(hashlib.sha512())
        return self._get_stream_hash()

    def get_sha384_hash(self, stream):
        self._set_stream(stream)
        self._set_hash_type(hashlib.sha384())
        return self._get_stream_hash()

    def get_sha256_hash(self, stream):
        self._set_stream(stream)
        self._set_hash_type(hashlib.sha256())
        return self._get_stream_hash()

    def get_sha224_hash(self, stream):
        self._set_stream(stream)
        self._set_hash_type(hashlib.sha224())
        return self._get_stream_hash()

    def get_sha1_hash(self, stream):
        self._set_stream(stream)
        self._set_hash_type(hashlib.sha1())
        return self._get_stream_hash()

    def get_md5_hash(self, stream):
        self._set_stream(stream)
        self._set_hash_type(hashlib.md5())
        return self._get_stream_hash()

    def _set_stream(self, stream):
        self._stream = stream

    def _set_hash_type(self, hash_type):
        self._hash = hash_type

    def _get_stream_hash(self):
        self._record_stream_cursor_location()
        self._set_location_to_file_start()
        self._update_hash()
        self._set_stream_to_recorded_cursor_position()
        return self._get_string_from_hash()

    def _record_stream_cursor_location(self):
        self._current = self._stream.tell()

    def _set_location_to_file_start(self):
        self._stream.seek(0)

    def _update_hash(self):
        for chunk in iter(lambda: self._stream.read(4096), b""):
            self._hash.update(chunk)

    def _set_stream_to_recorded_cursor_position(self):
        self._stream.seek(self._current)

    def _get_string_from_hash(self):
        return self._hash.hexdigest()
