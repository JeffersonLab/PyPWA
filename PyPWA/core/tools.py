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

import copy
import hashlib
import io
import logging
import os

import appdirs
import ruamel.yaml.comments

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ProcessOptions(object):

    _module_name = None
    _module_comment = None
    _option_comments = None
    _option_types = None
    _option_defaults = None
    _option_difficulties = None

    _built_options = None
    _required = None
    _optional = None
    _advanced = None

    def __init__(
            self, module, module_comment, options_comment,
            option_types, option_defaults, option_difficulty
    ):
        self._module_name = module
        self._module_comment = module_comment
        self._option_comments = options_comment
        self._option_types = option_types
        self._option_defaults = option_defaults
        self._option_difficulties = option_difficulty

        self._set_header_into_built_options()
        self._set_content_into_built_options()
        self._set_difficulties()

    def _set_header_into_built_options(self):
        header = ruamel.yaml.comments.CommentedMap()
        header.yaml_add_eol_comment(
            self._module_comment, self._module_name
        )
        self._built_options = header

    def _set_content_into_built_options(self):
        content = ruamel.yaml.comments.CommentedMap()
        populated_content = self._add_options_defaults(content)
        commented_content = self._add_option_comments(populated_content)
        self._built_options[self._module_name] = commented_content

    def _add_options_defaults(self, content):
        for option, value in self._option_defaults.items():
            content[option] = value
        return content

    def _add_option_comments(self, content):
        for option, comment in self._option_comments.items():
            content.yaml_add_eol_comment(comment, option)
        return content

    def _set_difficulties(self):
        self._make_separate_difficulties()
        self._process_separate_difficulties()

    def _make_separate_difficulties(self):
        required = copy.deepcopy(self._built_options)
        optional = copy.deepcopy(self._built_options)
        advanced = copy.deepcopy(self._built_options)

        self._required = required
        self._optional = optional
        self._advanced = advanced

    def _process_separate_difficulties(self):
        for option, difficulty in self._option_difficulties.items():
            if difficulty == "optional":
                self._required[self._module_name].pop(option)
            elif difficulty == "advanced":
                self._required[self._module_name].pop(option)
                self._optional[self._module_name].pop(option)

    @property
    def required(self):
        return self._required

    @property
    def optional(self):
        return self._optional

    @property
    def advanced(self):
        return self._advanced


class DataLocation(object):
    """
    Locates a place to store cache, logs, configuration, and data.
    """
    _cwd = os.getcwd()
    _found_uri = ""

    def get_cache_uri(self):
        possible_uri = appdirs.user_cache_dir("PyPWA", "JLab", __version__)
        self._find_usable_uri(possible_uri)
        return self._found_uri

    def get_data_uri(self):
        possible_uri = appdirs.user_data_dir("PyPWA", "JLab", __version__)
        self._find_usable_uri(possible_uri)
        return self._found_uri

    def get_log_uri(self):
        possible_uri = appdirs.user_log_dir("PyPWA", "JLab", __version__)
        self._find_usable_uri(possible_uri)
        return self._found_uri

    def get_config_uri(self):
        possible_uri = appdirs.user_config_dir("PyPWA", "JLab", __version__)
        self._find_usable_uri(possible_uri)
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


class FileHashString(object):

    _logger = logging.getLogger(__name__)
    _stream = io.FileIO
    _hash = hashlib.md5()
    _current = 0

    def __init__(self):
        """
        A simple utility that takes an io.open stream and returns its hash
        """
        self._logger.addHandler(logging.NullHandler())

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
