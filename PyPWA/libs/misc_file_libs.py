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
Miscellaneous file tools.
-------------------------
"""

import hashlib
import io
import os

import appdirs

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _CheckLocationIsUsable(object):

    def find_usable_uri(self, potential_uri):
        # type: (str) -> str
        self.__recursively_make_uri_directories(potential_uri)
        return self.__determine_potential_or_cwd(potential_uri)

    @staticmethod
    def __recursively_make_uri_directories(potential_uri):
        # type: (str) -> None
        try:
            os.makedirs(potential_uri)
        except OSError:
            pass

    def __determine_potential_or_cwd(self, potential_uri):
        # type: (str) -> str
        try:
            self.__check_writable(potential_uri)
            return potential_uri
        except OSError:
            self.__check_writable(os.getcwd())
            return os.getcwd()

    @staticmethod
    def __check_writable(potential_uri):
        # type: (str) -> None
        test_file = potential_uri + "/test"
        with open(test_file, "w") as stream:
            stream.write("test")
        os.remove(test_file)


def get_cache_uri():
    # type: () -> str
    possible_uri = appdirs.user_cache_dir("PyPWA", "JLab", __version__)
    usable_location = _CheckLocationIsUsable()
    return usable_location.find_usable_uri(possible_uri)


class _HashUtility(object):

    def get_stream_hash(self, file_location, file_hash):
        # type: (str, hashlib._hashlib.HASH) -> str
        with open(file_location, 'rb') as stream:
            self.__update_hash_with_file_contents(stream, file_hash)
        return self.__convert_hash_to_string(file_hash)

    @staticmethod
    def __update_hash_with_file_contents(stream, file_hash):
        # type: (io.FileIO, hashlib._hashlib.HASH) -> None
        for chunk in iter(lambda: stream.read(4096), b""):
            file_hash.update(chunk)

    @staticmethod
    def __convert_hash_to_string(file_hash):
        # type: (hashlib._hashlib.HASH) -> str
        return file_hash.hexdigest()


def get_sha512_hash(file_location):
    # type: (str) -> str
    hash_utility = _HashUtility()
    return hash_utility.get_stream_hash(file_location, hashlib.sha512())


class _FileLength(object):

    __BUFFER_SIZE = 1024 * 1024

    def __init__(self):
        self.__lines = 0  # type: int
        self.__buffer = b''  # type: bytes

    def get_length(self, file_location):
        # type: (str) -> int
        with io.open(file_location, 'rb') as binary_stream:
            self.__iterate_over_file(binary_stream)
        return self.__lines

    def __iterate_over_file(self, stream):
        # type: (io.FileIO) -> None
        self.__read_new_buffer(stream)
        while self.__buffer:
            self.__lines += self.__buffer.count(b'\n')
            self.__read_new_buffer(stream)

    def __read_new_buffer(self, stream):
        # type: (io.FileIO) -> None
        buffer = stream.raw.read(self.__BUFFER_SIZE)
        self.__check_old_buffer_for_missing_newline(buffer)
        self.__buffer = buffer

    def __check_old_buffer_for_missing_newline(self, buffer):
        # type: (bytes) -> None
        if not buffer and not self.__buffer.endswith(b'\n'):
            self.__lines += 1


def get_file_length(file_location):
    # type: (str) -> int
    counter = _FileLength()
    return counter.get_length(file_location)
