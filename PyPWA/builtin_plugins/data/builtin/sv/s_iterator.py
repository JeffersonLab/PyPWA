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
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core.templates import interface_templates


__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION

HEADER_SEARCH_BITS = 1024


class SvReader(interface_templates.ReaderInterfaceTemplate):

    def __init__(self, file_location):
        super(SvReader, self).__init__(file_location)
        self._previous_event = None  # type: collections.namedtuple
        self._reader = False  # type: csv.DictReader
        self._file = False  # type: io.TextIOBase
        self._types = False  # type: list[tuple]
        self._elements = False  # type: list[str]
        self._file_location = file_location

        self._start_input()

    def _start_input(self):
        if self._file:
            self._file.close()

        self._file = io.open(self._file_location)
        dialect = csv.Sniffer().sniff(
            self._file.read(HEADER_SEARCH_BITS), delimiters=[",", "\t"]
        )
        self._file.seek(0)

        self._reader = csv.reader(self._file, dialect)

        self._elements = next(self._reader)
        self._types = []
        for element in self._elements:
            self._types.append((element, "f8"))

    def reset(self):
        self._start_input()

    @property
    def next_event(self):
        non_parsed = list(next(self._reader))
        parsed = numpy.zeros(1, self._types)

        for index, element in enumerate(self._elements):
            parsed[element][0] = non_parsed[index]

        self._previous_event = parsed

        return self.previous_event

    @property
    def previous_event(self):
        return self._previous_event

    def close(self):
        self._file.close()


class SvWriter(interface_templates.WriterInterfaceTemplate):

    def __init__(self, file_location):
        super(SvWriter, self).__init__(file_location)
        self._file = open(file_location, "w")
        extension = file_location.split(".")[-1]

        if extension == "tsv":
            self._dialect = csv.excel_tab
        else:
            self._dialect = csv.excel

        self._writer = False  # type: cvs.DictWriter
        self._field_names = False  # type: list[str]

    def _writer_setup(self, data):
        if not self._writer:
            self._field_names = list(data.dtype.names)

            self._writer = csv.DictWriter(
                self._file,
                fieldnames=self._field_names,
                dialect=self._dialect
            )

            self._writer.writeheader()

    def write(self, data):
        self._writer_setup(data)

        dict_data = {}
        for field_name in self._field_names:
            dict_data[field_name] = repr(data[0][field_name])

        self._writer.writerow(dict_data)

    def close(self):
        self._file.close()
