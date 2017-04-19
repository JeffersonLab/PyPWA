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

    _stream = None  # type: io.FileIO

    def quick_test(self, file_location):
        self._set_stream(file_location)
        self._header_test()

    def full_test(self, file_location):
        self._set_stream(file_location)
        self._header_test()

    def _set_stream(self, file_location):
        self._stream = io.open(file_location, "r")

    def _header_test(self):
        header_test = _HeaderTest(self._stream)
        header_test.do_test()


class _HeaderTest(object):

    _logger = logging.getLogger(__name__)
    _stream = None  # type: io.FileIO
    _sniffer = None  # type: csv.Sniffer
    _sample = None  # type: str

    def __init__(self, stream):
        self._logger.addHandler(logging.NullHandler())
        self._stream = stream

    def do_test(self):
        self._set_sniffer()
        self._load_sample()
        self._header_test()
        self._reset_stream()

    def _set_sniffer(self):
        self._sniffer = csv.Sniffer()
        self._sniffer.preferred = ["/t", ","]

    def _load_sample(self):
        self._sample = self._stream.read(HEADER_SEARCH_BITS)

    def _header_test(self):
        if not self._has_a_header():
            raise exceptions.IncompatibleData(
                "CSV Module failed to find the files header in " +
                str(HEADER_SEARCH_BITS) + " characters!"
            )

    def _has_a_header(self):
        try:
            return self._sniffer.has_header(self._sample)
        except Exception as Error:
            self._logger.error(Error)
            return False

    def _reset_stream(self):
        self._stream.seek(0)
