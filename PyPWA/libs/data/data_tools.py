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
Holds various tools needed by the Data module.
"""

import os

import numpy

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class DataTypeSearch(object):
    """
    Object that searches for the best data wrapper 
    to use for the file in question
    """

    def search(self, file_location):
        """
        Search function, attempts multiple different search patterns to try
        to find a data type

        Args:
            file_location (str): The file that is to be parsed

        Returns:
            str: Type of File

        Raises:
            TypeError: If the file type can't be found

        See Also:
            Supported Data formats
        """

        result = self._extension_test(file_location)
        if result:
            return result

        result = self._line_test(file_location)
        if result:
            return result

        raise TypeError("File Type not known!")

    @staticmethod
    def _extension_test(file_location):
        """
        Attempts to find type based on file extension.

        Args:
            file_location (str): the file path

        Returns:
            str: Type of file if found.
            bool: False if no type is found
        """

        file_extension = os.path.splitext(file_location)[1].lower()

        if file_extension in ( ".csv", ".tsv"):
            return "sv"
        elif file_extension == ".yml":
            return "yaml"
        elif file_extension == ".pwa":
            return "pwa"
        else:
            return False

    @staticmethod
    def _line_test(file_location):
        """
        Loads the first line and checks it for patterns to
        try to determine the type.

        Args:
            file_location (str): the path to the file

        Returns:
            str: Type of file if found.
            bool: False if no type is found
        """
        with open(file_location, "r") as stream:
            first_line = stream.readline().strip("\n")

        if "=" in first_line or len(first_line) >= 1:
            return "kv"
        else:
            return 0


class DataTypeWrite(object):
    """
    Returns which writer to use based on the data.
    """
    @staticmethod
    def search(file_location):
        """
        Returns best writer based on data

        Args:
            file_location (str):

        Returns:
            str:
        """
        file_extension = os.path.splitext(file_location)[1].lower()

        if file_extension in (".tsv", ".csv"):
            return "sv"
        elif file_extension == ".yml":
            return "yaml"
        elif file_extension == ".pwa":
            return "pwa"
        else:
            return "kv"


class DataTypes(object):

    def type(self, data):
        if isinstance(data, numpy.ndarray):
            return self._arrays(data)
        elif isinstance(data, dict):
            return self._dicts(data)

    @staticmethod
    def _dicts(data):

        for key in data:
            if isinstance(data[key], dict):
                return "dictofdicts"
        return "dictofarrays"

    @staticmethod
    def _arrays(data):
        if isinstance(data[0], numpy.bool_):
            return "listofbools"
        else:
            return "listoffloats"
