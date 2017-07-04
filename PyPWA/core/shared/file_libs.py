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
Miscellaneous File Libraries
----------------------------
- _FileLength - An object that searches files in binary to quickly determine
  the length of a file.
- get_file_length - The function wrapping _FileLength
"""

import io

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _FileLength(object):

    __BUFFER_SIZE = 1024*1024

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
