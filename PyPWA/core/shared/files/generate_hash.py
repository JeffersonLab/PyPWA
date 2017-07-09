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
import io

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


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
