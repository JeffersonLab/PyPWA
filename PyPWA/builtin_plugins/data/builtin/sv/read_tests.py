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

import csv
import io
import logging

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.builtin_plugins.data import data_templates
from PyPWA.builtin_plugins.data import exceptions

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION

HEADER_SEARCH_BITS = 1024


class SvDataTest(data_templates.ReadTest):

    _stream = None  # type: io.FileIO

    def quick_test(self, file_location):
        self._set_stream(file_location)
        self._header_test()
        self._comparison_test(5)

    def full_test(self, file_location):
        self._set_stream(file_location)
        self._header_test()
        self._comparison_test()

    def _set_stream(self, file_location):
        self._stream = io.open(file_location, "r")

    def _header_test(self):
        header_test = _HeaderTest(self._stream)
        header_test.do_test()

    def _comparison_test(self, lines=0):
        comparison_test = _CountTest(self._stream, lines)
        comparison_test.do_test()


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
            raise exceptions.IncompatibleData

    def _reset_stream(self):
        self._stream.seek(0)


class _CountTest(object):

    _logger = logging.getLogger(__name__)
    _stream = None  # type: io.FileIO
    _comma_count = 0
    _tab_count = 0
    _break_count = 0

    def __init__(self, stream, count):
        self._logger.addHandler(logging.NullHandler())
        self._stream = stream
        self._break_count = count

    def do_test(self):
        self._count_test()
        self._reset_stream()

    def _count_test(self):
        for index, line in enumerate(self._stream):
            if self._should_break(index):
                break
            self._begin_test(line)

    def _should_break(self, index):
        if not self._break_count == 0 and self._break_count == index:
            return True
        else:
            return False

    def _begin_test(self, line):
        if self._zeroed():
            self._set_counts(line)
        self._do_comparison(line)

    def _zeroed(self):
        if self._comma_count == 0 and self._tab_count == 0:
            return True
        else:
            return False

    def _set_counts(self, line):
        self._tab_count = len(line.split("\t"))
        self._comma_count = len(line.split(","))

    def _do_comparison(self, line):
        if not self._tab_count == 0:
            self._compare_tabs(line)
        elif not self._comma_count == 0:
            self._compare_commas(line)
        else:
            raise exceptions.IncompatibleData

    def _compare_tabs(self, line):
        self._compare_counts(line, "\t", self._tab_count)

    def _compare_commas(self, line):
        self._compare_counts(line, ",", self._comma_count)

    @staticmethod
    def _compare_counts(line, delimiter, original_count):
        count = len(line.split(delimiter))
        if not count == original_count:
            raise exceptions.IncompatibleData

    def _reset_stream(self):
        self._stream.seek(0)
