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

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import internals

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


HEADER_SEARCH_BITS = 1024


class SvReader(internals.Reader):

    _previous_event = None  # type: collections.namedtuple
    _reader = False  # type: csv.DictReader
    _file = False  # type: io.TextIOBase
    _types = False  # type: list[tuple]
    _elements = False  # type: list[str]

    def __init__(self, file_location):
        self._the_file = file_location
        self._set_file_location(file_location)
        self._start_input()

    def _set_file_location(self, file_location):
        self._file_location = file_location

    def _start_input(self):
        self._set_file()
        dialect = self._get_dialect()
        self._set_reader(dialect)
        self._set_elements()
        self._set_numpy_types()

    def _set_file(self):
        self._file = io.open(self._file_location)

    def _get_dialect(self):
        dialect = csv.Sniffer().sniff(
            self._file.read(HEADER_SEARCH_BITS), delimiters=[",", "\t"]
        )
        self._file.seek(0)
        return dialect

    def _set_reader(self, dialect):
        self._reader = csv.reader(self._file, dialect)

    def _set_elements(self):
        self._elements = next(self._reader)

    def _set_numpy_types(self):
        self._types = []
        for element in self._elements:
            self._types.append((element, "f8"))

    def close(self):
        self._file.close()

    def next(self):
        non_parsed = list(next(self._reader))
        parsed = numpy.zeros(1, self._types)

        for index, element in enumerate(self._elements):
            parsed[element][0] = non_parsed[index]

        self._previous_event = parsed

        return self._previous_event


class SvWriter(internals.Writer):

    _dialect = csv.Dialect
    _writer = csv.DictWriter
    _field_names = [str]

    def __init__(self, file_location):
        self._the_file = file_location
        self._file = open(file_location, "w")
        self._set_dialect(file_location)

    def _set_dialect(self, file_location):
        if self._is_tab(file_location):
            self._dialect = csv.excel_tab
        else:
            self._dialect = csv.excel

    def _is_tab(self, file_location):
        return self._get_extension(file_location) == ".tsv"

    @staticmethod
    def _get_extension(file_location):
        return file_location.split(".")[-1]

    def write(self, data):
        self._writer_setup(data)
        converted_data = self._convert_to_dict(data)
        self._write_row(converted_data)

    def _writer_setup(self, data):
        if not self._writer:
            self._set_field_names(data)
            self._set_writer()
            self._write_header()

    def _set_field_names(self, data):
        self._field_names = list(data.dtype.names)

    def _set_writer(self):
        self._writer = csv.DictWriter(
            self._file,
            fieldnames=self._field_names,
            dialect=self._dialect
        )

    def _write_header(self):
        self._writer.writeheader()

    def _convert_to_dict(self, data):
        dict_data = {}
        for field_name in self._field_names:
            dict_data[field_name] = repr(data[0][field_name])
        return dict_data

    def _write_row(self, dict_data):
        self._writer.writerow(dict_data)

    def close(self):
        self._file.close()
