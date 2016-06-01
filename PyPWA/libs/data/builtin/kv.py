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
Handles KV to / from memory.

The objects in this file are dedicated to reading the EVIL files from disk and
into memory. This file type is being depreciated for many reasons, and will live
here until it shrivels away, is completely forgotten, and dies.
"""

import collections
import io

import numpy

from PyPWA.configuratr import data_types
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class KvInterface(object):

    def parse(self, file_location):
        raise NotImplementedError()

    @staticmethod
    def write(file_location, data):
        raise NotImplementedError()

    @staticmethod
    def file_length(file_location):
        """
        Determines the number of lines in the file.

        Args:
            file_location (str): The file to check for line _count.

        Returns:
            int: The number of lines.
        """
        with io.open(file_location) as stream:
            for file_length, line in enumerate(stream):
                pass
        return file_length + 1


class DictOfArrays(KvInterface):
    """
    Handles old Kv format
    """

    def parse(self, file_location):
        """
        Loads Kv data into memory

        Args:
            file_location (str): Path of file

        Returns:
            dict: name : numpy array of events
        """

        file_length = self.file_length(file_location)

        with open(file_location) as stream:
            first_line = stream.readline()

        parsed = {}

        for x in range(len(first_line.split(","))):
            parsed[first_line.split(",")[x].split("=")[0]] = numpy.zeros(
                shape=file_length, dtype="float64"
            )

        with io.open(file_location) as stream:
            for index, line in enumerate(stream):
                for particle_count in range(len(line.split(","))):
                    parsed[line.split(",")[particle_count].split(
                        "=")[0]][index] = numpy.float64(line.strip("\n").split(
                        ",")[particle_count].split("=")[1])

        event = data_types.GenericEvent(list(parsed.keys()))
        final = event.make_particle(parsed)
        return final

    @staticmethod
    def write(file_location, data):
        """
        Writes Classic Kvs to file

        Args:
            file_location (str): path to file
            data (collections.namedtuple): dict of numpy arrays
        """

        kvars = data.standard_parsed_values
        the_data = data._asdict()

        with open(file_location, "w") as stream:
            for event in range(len(the_data[kvars[0]])):
                line = ""
                for kvar in range(len(kvars)):
                    if kvar > 0:
                        line += ","
                    line += "{0}={1}".format(kvars[kvar], str(
                        the_data[kvars[kvar]][event]
                    ))
                line += "\n"
                stream.write(line)


class ListOfFloats(KvInterface):
    """
    Handles QFactor list parsing
    """

    def parse(self, file_location):
        """
        Parses a list of factors

        Args:
            file_location (str): The path to file

        Returns:
            numpy.ndarray: Array of factors
        """

        file_length = self.file_length(file_location)

        parsed = numpy.zeros(shape=file_length, dtype="float64")

        with io.open(file_location) as stream:
            for count, line in enumerate(stream):
                parsed[count] = line.strip("\n")
        return parsed

    @staticmethod
    def write(file_location, data):
        """
        Writes Arrays to disk as floats

        Args:
            file_location (str): Path to file
            data (numpy.ndarray): Data to be written to disk
        """
        with open(file_location, "w") as stream:
            for event in data:
                stream.write(str(event) + "\n")


class ListOfBooleans(KvInterface):
    """
    Classic boolean per line data type
    """

    def parse(self, file_location):
        """
        Parses list of booleans into numpy array.

        Args:
            file_location (str): Path to file

        Returns:
            numpy.ndarray: Bool array of weights
        """

        file_length = self.file_length(file_location)

        weights = numpy.zeros(shape=file_length, dtype=bool)

        with io.open(file_location) as stream:
            for index, weight in enumerate(stream):
                weights[index] = int(weight)

        return weights

    @staticmethod
    def write(file_location, data):
        """
        Writes booleans to text file with each weight on a new line

        Args:
            file_location (str): Path to file
            data (numpy.ndarray): Array of booleans
        """
        with open(file_location, "w") as stream:
            for weight in data:
                stream.write(str(int(weight)) + "\n")


class SomewhatIntelligentSelector(KvInterface):
    """
    Attempts to select the write object to load and write Expanded Variable
    Identification Lists to and from the disk. It does this by examining the
    EVIL data and using its types to select the EVIL object.
    """
    def parse(self, file_location):
        """
        Reads in EVIL format from disk, searches the first line of data for
        clues as to the data type. If there are = or , in the first line it
        assumes its a list of dict, if . then float, and if none of the above
        pure bool.

        If it doesn't work, perhaps use CSV?
        Args:
            file_location (str): The location of the file that needs to be read
                in from the disk.

        Returns:
            data_types.GenericEvent:  The data that was parsed from the disk.

        """
        the_file = io.open(file_location)
        first_line = the_file.readline()
        if "=" or "," in first_line:
            parser = DictOfArrays()
        elif "." in first_line:
            parser = ListOfFloats()
        else:
            parser = ListOfBooleans()

        return parser.parse(file_location)

    @staticmethod
    def write(file_location, data):
        """
        Writes EVIL data types to disk, detects the data in the same way that
        parse works, however does it by running the type check against the
        object that was received.

        Args:
            file_location (str): Where to write the data.
            data (collections.namedtuple | numpy.ndarray): The data that needs
                to be written to disk.
        """
        if isinstance(data, dict):
            writer = DictOfArrays()
        elif isinstance(data[0], numpy.float64):
            writer = ListOfFloats()
        else:
            writer = ListOfBooleans()
        writer.write(file_location, data)

metadata_data = {
    "extension": "txt",
    "validator": None,
    "reader": None,
    "writer": None,
    "memory": SomewhatIntelligentSelector
}