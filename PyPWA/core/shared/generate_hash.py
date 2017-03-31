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
This will take a str to a file location, then parse the entire file, returning
the hash of that file. Hashes are useful for detecting changes in a file 
without comparing the enclosed data directly.
"""

import hashlib

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


def get_sha512_hash(file_location):
    return __get_stream_hash(file_location, hashlib.sha512())


def get_sha384_hash(file_location):
    return __get_stream_hash(file_location, hashlib.sha384())


def get_sha256_hash(file_location):
    return __get_stream_hash(file_location, hashlib.sha256())


def get_sha224_hash(file_location):
    return __get_stream_hash(file_location, hashlib.sha224())


def get_sha1_hash(file_location):
    return __get_stream_hash(file_location, hashlib.sha1())


def get_md5_hash(file_location):
    return __get_stream_hash(file_location, hashlib.md5())


def __get_stream_hash(file_location, file_hash):
    stream = __open_stream(file_location)
    __update_hash(stream, file_hash)
    __close_stream(stream)
    return __get_string_from_hash(file_hash)


def __open_stream(file_location):
    return open(file_location, "rb")


def __update_hash(stream, file_hash):
    for chunk in iter(lambda: stream.read(4096), b""):
        file_hash.update(chunk)


def __close_stream(stream):
    stream.close()


def __get_string_from_hash(file_hash):
    return file_hash.hexdigest()
