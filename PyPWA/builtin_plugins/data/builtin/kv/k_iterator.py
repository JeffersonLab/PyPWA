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
Handles EVIL to / from memory.

The objects in this file are dedicated to reading the EVIL files from disk
and into memory. This file type is being depreciated for many reasons, and
will live here until it shrivels away, is completely forgotten, and dies.

EVIL, Expanded Variable Identification Lists, earned their name from their
inefficient nature when it comes to reading in, writing out, or simply
existing, its a name given to these EVIL formats out of a mixture of spite
and love by current and former developers alike.

This format exists currently only as backwards compatibility, and may not
be bug free or entirely optimized, and may never be. If you are a user
trying to figure out what you should export your data to, or a developer
trying to learn the nature of data within PyPWA, you should move your
attention to CSV/TSV in the SV object and forget that this ever existed.
"""

import io
import logging

import numpy

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core.templates import interface_templates
from PyPWA.builtin_plugins.data.builtin.kv import k_read_tests

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class EVILReader(interface_templates.ReaderInterfaceTemplate):

    def __init__(self, file_location):
        """
        Reads in the EVIL Type one event at a time.

        Args:
            file_location (str): The location of the EVIL file.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        super(EVILReader, self).__init__(file_location)
        self._previous_event = None
        self._file = False  # type: io.TextIOBase
        self._parameters = False  # type: [str]
        self._file_data_type = False  # type: str

        self._start_input()

    def _start_input(self):
        """
        This file completely resets the the file handler if it exists and
        creates it otherwise.
        """
        if self._file:
            self._file.close()

        self._file = io.open(self._the_file, "rt")

        if not isinstance(self._file_data_type, str):
            self._set_data_type()
        if not isinstance(self._parameters, list):
            self._build_params()

    def _build_params(self):
        """
        Searches for the parameters in the file then sets them to
        self._parameters.
        """
        first_line = self._file.readline()

        if self._file_data_type == "DictOfArrays":
            self._parameters = []
            for parameter in first_line.split(","):
                self._parameters.append(parameter.split("=")[0])

        elif self._file_data_type == "ListOfBools":
            self._parameters = ["bools"]

        elif self._file_data_type == "ListOfFloats":
            self._parameters = ["floats"]

        self._file.seek(0)

    def _set_data_type(self):
        """
        Sets self._file_data_type using the validator object. Mostly
        Accurate.
        """
        validator = k_read_tests.EVILDataTest()
        validator.quick_test(self._the_file)
        self._file_data_type = validator.evil_type

    def reset(self):
        """
        Wrapper for _start_input
        """
        self._start_input()

    @property
    def next_event(self):
        """
        Reads in a single line and parses the line into a GenericEvent.

        Returns:
            numpy.ndarray: The values of the array.
        """
        if self._file_data_type == "DictOfArrays":
            values = self._read_dict()
        elif self._file_data_type == "ListOfBools":
            values = self._read_bool()
        else:
            values = self._read_float()

        self._previous_event = values
        return self._previous_event

    @property
    def previous_event(self):
        return self.previous_event

    def __read(self):
        """
        Reads a single line from the file and removes the spaces and
        newline.

        Raises:
            StopIteration: Raised when there is no data left in the file.

        Returns:
            str: The read in line without spaces and newlines.
        """
        string = self._file.readline().strip("\n").strip(" ")
        if string == "":
            raise StopIteration
        return string

    def _read_bool(self):
        """
        Reads a single line and returns the bool value from that line.

        Returns:
            numpy.ndarray: True or False depending on the value of the
                line that was read.
        """
        x = numpy.zeros(1, bool)
        x[0] = bool(self.__read())
        return x

    def _read_float(self):
        """
        Reads a single line and returns the float value from the line.

        Returns:
            numpy.ndarray: The value read in from the file.
        """
        x = numpy.zeros(1, "f8")
        x[0] = numpy.float64(self.__read())
        return x

    def _read_dict(self):
        """
        Reads a single line and returns the list of the values rendered
        from the file.

        Returns:
            numpy.ndarray: The values read in from the file.
        """
        the_line = self.__read()
        self._logger.debug("Found: " + the_line)

        names = []
        for variable in the_line.split(","):
            names.append(variable.split("=")[0])

        types = []
        for name in names:
            types.append((str(name), "f8"))

        self._logger.debug("Numpy Types = " + repr(types))

        final = numpy.zeros(1, types)

        for variable in the_line.split(","):
            value = numpy.float64(variable.split("=")[1])
            name = variable.split("=")[0]
            final[0][name] = value

        return final

    def close(self):
        self._file.close()


class EVILWriter(interface_templates.WriterInterfaceTemplate):

    def __init__(self, file_location):
        """
        Single event writer for EVIL data types. Writes a single event at
        a time and leaves the file handle open until its explicitly closed
        by the developer or user.

        Args:
            file_location (str): Where to write the data.
        """
        super(EVILWriter, self).__init__(file_location)
        self._file = io.open(file_location, "w")

    def write(self, data):
        """
        Writes a single event to file at a time.

        Args:
            data (numpy.ndarray): The array that contains the data to be
                writen to the file.
        """
        string = u""
        for index, key in enumerate(list(data.dtype.names)):
            if not index == 0:
                string += u","
            string += str(key) + u"=" + repr(data[0][key])
        string += u"\n"

        self._file.write(string)

    def close(self):
        """
        Closes the file safely.
        """
        self._file.close()

