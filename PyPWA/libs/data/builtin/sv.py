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

from PyPWA.configurator import data_types
from PyPWA.libs.data import definitions
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION

HEADER_SEARCH_BITS = 1024


class SvMemory(definitions.TemplateMemory):
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
            collections.namedtuple: The tuple containing the data parsed
                in from the file.
        """
        with io.open(file_location, "rt") as stream:
            for line_count, throw in enumerate(stream):
                pass

        with io.open(file_location, "rt") as stream:
            dialect = csv.Sniffer().sniff(stream.read(HEADER_SEARCH_BITS))
            stream.seek(0)

            sv = csv.reader(stream, dialect)

            elements = next(sv)
            parsed = {}
            for element in elements:
                parsed[element] = numpy.zeros(
                    shape=line_count, dtype="float64"
                )

            for index, row in enumerate(sv):
                for count in range(len(row)):
                    parsed[elements[count]][index] = row[count]
        event = data_types.GenericEvent(list(parsed.keys()))
        final = event.make_particle(list(parsed.values()))

        return final

    def write(self, file_location, data):
        """
        Writes the data from memory to file.

        Args:
            file_location  (str): Where to write the data to.
            data (collections.namedtuple): Dictionary of the arrays
                containing the data.
        """
        extension = file_location.split(".")[-1]

        if extension == "tsv":
            the_dialect = csv.excel_tab
        else:
            the_dialect = csv.excel

        with io.open(file_location, "wt") as stream:
            field_names = list(data._asdict().keys())

            writer = csv.DictWriter(stream, fieldnames=field_names,
                                    dialect=the_dialect)
            writer.writeheader()

            for index in range(len(data._asdict()[field_names[0]])):
                temp = {}
                for field in field_names:
                    temp[field] = repr(data._asdict()[field][index])
                writer.writerow(temp)


class SvReader(definitions.TemplateReader):

    def __init__(self, file_location):
        """
        This reads in SV Files a single event at a time from disk, then
        puts the contents into a GenericEvent Container.

        Args:
            file_location (str): The location of the file to read in.
        """
        super(SvReader, self).__init__(file_location)
        self._previous_event = None  # type: collections.namedtuple
        self._master_particle = False  # type: data_types.GenericEvent
        self._reader = False  # type: csv.DictReader
        self._file = False  # type: io.TextIOBase

        self._start_input()

    def _start_input(self):
        """
        Starts the input and configures the reader. Detects the files
        dialect and plugs the header information into the GenericEvent.
        """
        if self._file:
            self._file.close()

        dialect = csv.Sniffer().sniff(self._file.read(HEADER_SEARCH_BITS))
        self._file.seek(0)

        self._reader = csv.reader(self._file, dialect)

        elements = next(self._reader)
        self._master_particle = data_types.GenericEvent(elements)

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
            list[numpy.float64]: The data read in from the event.
        """
        un_parsed = list(next(self._reader))
        parsed = []
        for parse in un_parsed:
            parsed.append(numpy.float64(parse))

        self._previous_event = self._master_particle.make_particle(parsed)

        return self.previous_event

    @property
    def previous_event(self):
        return self._previous_event

    def close(self):
        self._file.close()


class SvWriter(definitions.TemplateWriter):

    def __init__(self, file_location):
        """
        Object writes data to file in either a tab separated sheet or a
        comma separated sheet.

        Args:
            file_location (str): Location to  write the data to.
        """
        super(SvWriter, self).__init__(file_location)
        self._file = io.open(file_location, "w")

        extension = file_location.split(".")[-1]

        if extension == "tsv":
            self._dialect = csv.excel_tab
        else:
            self._dialect = csv.excel

        self._count = 0

    def write(self, data):
        """
        Writes the data to a SV Sheet a single event at a time.

        Args:
            data (collections.named_tuple): The tuple containing the data
                that needs to be written.
        """
        field_names = list(data._asdict().keys())

        writer = csv.DictWriter(self._file, fieldnames=field_names,
                                dialect=self._dialect)
        if self._count == 0:
            writer.writeheader()

        writer.writerow(data._asdict())
        self._count += 1

    def close(self):
        """
        Properly closes the file handle.
        """
        self._file.close()


class SvValidator(definitions.TemplateValidator):

    def __init__(self, file_location, full=False):
        """
        Simple testing object that tries to validate the file, ensures
        that the object can read the file before parsing begins.

        Args:
            file_location (str): The location of the file that needs to
                validated.
            full (bool): Whether the entire file should be tested or not.
        """
        super(SvValidator, self).__init__(file_location, full)
        self._file = io.open(file_location, "rt")

    def _check_header(self):
        """
        Simple test to see if the header for the file is a valid
        CSV Header.
        """
        if not csv.Sniffer().has_header(
                self._file.read(HEADER_SEARCH_BITS)
        ):
            raise definitions.IncompatibleData(
                "CSV Module failed to find the files header in " +
                str(HEADER_SEARCH_BITS) + " characters!"
            )

    def test(self):
        self._check_header()

metadata_data = {
    "name": "Sv",
    "extensions": [".tsv", ".csv"],
    "validator": SvValidator,
    "reader": SvReader,
    "writer": SvWriter,
    "memory": SvMemory
}