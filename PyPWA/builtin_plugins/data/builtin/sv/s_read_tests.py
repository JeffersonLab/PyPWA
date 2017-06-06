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

import csv
import io
import logging

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import data_templates
from PyPWA.builtin_plugins.data import exceptions

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


HEADER_SEARCH_BITS = 3072


class SvDataTest(data_templates.ReadTest):

    def __init__(self):
        self.__stream = None  # type: io.FileIO

    def quick_test(self, file_location):
        # type: (str) -> None
        self.__set_stream(file_location)
        self.__header_test()

    def full_test(self, file_location):
        # type: (str) -> None
        self.__set_stream(file_location)
        self.__header_test()

    def __set_stream(self, file_location):
        # type: (str) -> None
        self.__stream = io.open(file_location, "r")

    def __header_test(self):
        header_test = _HeaderTest(self.__stream)
        header_test.do_test()


class _HeaderTest(object):

    __LOGGER = logging.getLogger(__name__ + "._HeaderTest")

    def __init__(self, stream):
        # type: (io.FileIO) -> None
        self.__stream = stream
        self.__sniffer = None  # type: csv.Sniffer
        self.__sample = None  # type: str

    def do_test(self):
        self.__set_sniffer()
        self.__load_sample()
        self.__header_test()
        self.__reset_stream()

    def __set_sniffer(self):
        self.__sniffer = csv.Sniffer()
        self.__sniffer.preferred = ["/t", ","]

    def __load_sample(self):
        self.__sample = self.__stream.read(HEADER_SEARCH_BITS)

    def __header_test(self):
        if not self.__has_a_header():
            raise exceptions.IncompatibleData(
                "CSV Module failed to find the files header in " +
                str(HEADER_SEARCH_BITS) + " characters!"
            )

    def __has_a_header(self):
        # type: () -> bool
        try:
            return self.__sniffer.has_header(self.__sample)
        except Exception as Error:
            self.__LOGGER.error(Error)
            return False

    def __reset_stream(self):
        self.__stream.seek(0)
