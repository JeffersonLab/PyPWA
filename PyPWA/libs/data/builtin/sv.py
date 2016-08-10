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

"""
Handles SV to / from memory.

The objects in this file are dedicated to reading SV files to memory and
writing data to SV to disk. This is the preferred and default method of
handling data to disk as of version PyPWA 2.0.0
"""

import csv
import collections
import io

import numpy

from PyPWA.configurator import templates
from PyPWA.libs.data import data_templates
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION

HEADER_SEARCH_BITS = 1024  # type: int


class SvMemory(data_templates.TemplateMemory):
    """
    Object for reading and writing delimiter separated data files.
    """

    def parse(self, file_location):
        """
        Reads a delimiter separated file containing data from disk.

        Args:
            file_location (str): The file that contain the data to be
                read.
        Returns:
            numpy.ndarray: The tuple containing the data parsed in from
                the file.
        """
        with io.open(file_location, "rt") as stream:
            for line_count, throw in enumerate(stream):
                pass

        with io.open(file_location, "rt") as stream:
            dialect = csv.Sniffer().sniff(stream.read(HEADER_SEARCH_BITS))
            stream.seek(0)

            sv = csv.reader(stream, dialect)

            elements = next(sv)

            types = []
            for element in elements:
                types.append((element, "f8"))

            parsed = numpy.zeros(line_count, types)

            for index, row in enumerate(sv):
                for count in range(len(row)):
                    parsed[elements[count]][index] = row[count]

        return parsed

    def write(self, file_location, data):
        """
        Writes the data from memory to file.

        Args:
            file_location  (str): Where to write the data to.
            data (numpy.ndarray): Dictionary of the arrays
                containing the data.
        """
        extension = file_location.split(".")[-1]

        if extension == "tsv":
            the_dialect = csv.excel_tab
        else:
            the_dialect = csv.excel

        with open(file_location, "wt") as stream:
            field_names = list(data.dtype.names)

            writer = csv.DictWriter(stream, fieldnames=field_names,
                                    dialect=the_dialect)
            writer.writeheader()

            for index in range(len(data[field_names[0]])):
                temp = {}
                for field in field_names:
                    temp[field] = repr(data[field][index])
                writer.writerow(temp)


class SvReader(data_templates.ReaderTemplate):

    def __init__(self, file_location):
        """
        This reads in SV Files a single event at a time from disk, then
        puts the contents into a GenericEvent Container.

        Args:
            file_location (str): The location of the file to read in.
        """
        super(SvReader, self).__init__(file_location)
        self._previous_event = None  # type: collections.namedtuple
        self._reader = False  # type: csv.DictReader
        self._file = False  # type: io.TextIOBase
        self._types = False  # type: list[tuple]
        self._elements = False  # type: list[str]
        self._file_location = file_location

        self._start_input()

    def _start_input(self):
        """
        Starts the input and configures the reader. Detects the files
        dialect and plugs the header information into the GenericEvent.
        """
        if self._file:
            self._file.close()

        self._file = io.open(self._file_location)
        dialect = csv.Sniffer().sniff(self._file.read(HEADER_SEARCH_BITS))
        self._file.seek(0)

        self._reader = csv.reader(self._file, dialect)

        self._elements = next(self._reader)
        self._types = []
        for element in self._elements:
            self._types.append((element, "f8"))

    def reset(self):
        """
        Calls the _start_input method to properly close then reopen the
        file handle and restart the CSV process.
        """
        self._start_input()

    @property
    def next_event(self):
        """
        Simple read method that takes the list that is received from the
        CSV reader, translates it from text to numpy.float64, then returns
        the final data

        Returns:
            numpy.ndarray: The data read in from the event.
        """
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


class SvWriter(data_templates.WriterTemplate):

    def __init__(self, file_location):
        """
        Object writes data to file in either a tab separated sheet or a
        comma separated sheet.

        Args:
            file_location (str): Location to  write the data to.
        """
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
        """
        Writes the data to a SV Sheet a single event at a time.

        Args:
            data (numpy.ndarray): The tuple containing the data
                that needs to be written.
        """
        self._writer_setup(data)

        dict_data = {}
        for field_name in self._field_names:
            dict_data[field_name] = repr(data[0][field_name])

        self._writer.writerow(dict_data)

    def close(self):
        """
        Properly closes the file handle.
        """
        self._file.close()


class SvDataPlugin(data_templates.TemplateDataPlugin):

    def __init__(self, file_location, full=False):
        """
        Simple testing object that tries to validate the file, ensures
        that the object can read the file before parsing begins.

        Args:
            file_location (str): The location of the file that needs to
                validated.
            full (bool): Whether the entire file should be tested or not.
        """
        super(SvDataPlugin, self).__init__(file_location, full)
        self._file = io.open(file_location, "rt")

    def _check_header(self):
        """
        Simple test to see if the header for the file is a valid
        CSV Header.
        """
        if not csv.Sniffer().has_header(
                self._file.read(HEADER_SEARCH_BITS)
        ):
            raise templates.IncompatibleData(
                "CSV Module failed to find the files header in " +
                str(HEADER_SEARCH_BITS) + " characters!"
            )

    def test(self):
        self._check_header()

metadata_data = {
    "name": "Sv",
    "extensions": [".tsv", ".csv"],
    "validator": SvDataPlugin,
    "reader": SvReader,
    "writer": SvWriter,
    "memory": SvMemory
}