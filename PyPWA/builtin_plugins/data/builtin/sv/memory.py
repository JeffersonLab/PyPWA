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
import os

import numpy
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.builtin_plugins.data import data_templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION

HEADER_SEARCH_BITS = 1024


class SvMemory(data_templates.TemplateMemory):

    def parse(self, file_location):
        parser = _SvParser()
        return parser.return_read_data(file_location)

    def write(self, file_location, data):
        writer = _SvMemoryWriter()
        writer.write_memory_to_disk(file_location, data)


class _SvParser(object):

    _logger = logging.getLogger(__name__)
    _line_count = 0
    _dialect = None
    _stream = None
    _reader = None
    _header = None

    def __init__(self):
        self._logger.addHandler(logging.NullHandler())

    def return_read_data(self, file_location):
        self._open_stream(file_location)
        self._set_required_data()
        data = self._parse_data()
        self._close_stream()
        return data

    def _set_line_number(self):
        for self._line_count, throw_away in enumerate(self._stream):
            pass
        self._reset_stream()

    def _open_stream(self, file_location):
        self._stream = io.open(file_location, "r")

    def _reset_stream(self):
        self._stream.seek(0)

    def _close_stream(self):
        self._stream.close()

    def _set_required_data(self):
        self._set_line_number()
        self._set_dialect()
        self._set_reader()
        self._set_header()

    def _set_dialect(self):
        self._dialect = csv.Sniffer().sniff(
            self._stream.read(HEADER_SEARCH_BITS), delimiters=[",", "\t"]
        )
        self._reset_stream()

    def _set_reader(self):
        self._reader = csv.reader(self._stream, self._dialect)

    def _set_header(self):
        self._header = next(self._reader)

    def _parse_data(self):
        empty_array = self._setup_numpy_array()
        return self._fill_array(empty_array)

    def _setup_numpy_array(self):
        types = self._build_numpy_types()
        return self._make_empty_numpy_array(types)

    def _build_numpy_types(self):
        types = []
        for column in self._header:
            types.append((column, "f8"))

        self._logger.debug("Types: " + repr(types))
        return types

    def _make_empty_numpy_array(self, dtype):
        return numpy.zeros(self._line_count, dtype)

    def _fill_array(self, empty_array):
        for row_index, row_data in enumerate(self._reader):
            self._fill_row(empty_array, row_index, row_data)
        return empty_array

    def _fill_row(self, array, row_index, row_data):
        for column_index in range(len(row_data)):
            array[self._header[column_index]][row_index] = \
                row_data[column_index]


class _SvMemoryWriter(object):

    _dialect = ""
    _column_names = None
    _stream = None
    _writer = None

    def write_memory_to_disk(self, file_location, data):
        self._setup_basic_data(file_location, data)
        self._setup_writer(file_location)
        self._write_data(data)

    def _setup_basic_data(self, file_location, data):
        self._process_dialect(file_location)
        self._set_column_names(data)

    def _process_dialect(self, file_location):
        extension = self._get_extension(file_location)
        self._set_dialect(extension)

    @staticmethod
    def _get_extension(file_location):
        return os.path.splitext(file_location)[1]

    def _set_dialect(self, extension):
        if extension == ".tsv":
            self._dialect = csv.excel_tab
        else:
            self._dialect = csv.excel

    def _set_column_names(self, data):
        self._column_names = data.dtype.names

    def _setup_writer(self, file_location):
        self._open_stream(file_location)
        self._set_writer()
        self._write_header()

    def _open_stream(self, file_location):
        self._stream = io.open(file_location, "w")

    def _set_writer(self):
        self._writer = csv.DictWriter(
            self._stream, fieldnames=self._column_names, dialect=self._dialect
        )

    def _write_header(self):
        self._writer.writeheader()

    def _write_data(self, data):
        for index in self._iterator_over_columns(data):
            new_dict = self._convert_row_to_dict(index, data)
            self._writer.writerow(new_dict)

    def _iterator_over_columns(self, data):
        length = len(data[self._column_names[0]])
        return range(length)

    def _convert_row_to_dict(self, row_index, data):
        new_dict = {}
        for column in self._column_names:
            new_dict[column] = repr(data[column][row_index])
        return new_dict
