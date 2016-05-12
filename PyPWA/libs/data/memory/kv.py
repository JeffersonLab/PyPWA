# The MIT License (MIT)
#
# Copyright (c) 2014-2016 JLab.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Handles KV to / from memory.

The objects in this file are dedicated to reading the EVIL files from disk and
into memory. This file type is being depreciated for many reasons, and will live
here until it shrivels away, is completely forgotten, and dies.
"""

import io

import numpy

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
            file_location (str): The file to check for line count.

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
        return parsed

    @staticmethod
    def write(file_location, data):
        """
        Writes Classic Kvs to file

        Args:
            file_location (str): path to file
            data (dict): dict of numpy arrays
        """

        kvars = list(data)

        with open(file_location, "w") as stream:
            for event in range(len(data[kvars[0]])):
                line = ""
                for kvar in range(len(kvars)):
                    if kvar > 0:
                        line += ","
                    line += "{0}={1}".format(kvars[kvar], str(
                        data[kvars[kvar]][event]
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
