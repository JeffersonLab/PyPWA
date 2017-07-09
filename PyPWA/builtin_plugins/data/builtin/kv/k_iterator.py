#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016 JLab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

import logging

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.interfaces import data_loaders
from PyPWA.libs.files import line_count

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class EVILReader(data_loaders.Reader):

    __LOGGER = logging.getLogger(__name__ + ".EVILReader")

    def __init__(self, file_location):
        self.__event_count = line_count.get_file_length(file_location)
        self.__file = open(file_location)
        self.__column_names = None
        self.__numpy_type = None
        self.__setup_static_information()

    def __setup_static_information(self):
        columns = self.__get_columns()
        self.__column_names = self.__get_names(columns)
        self.__numpy_type = self.__get_numpy_type()
        self.__file.seek(0)

    def __get_columns(self):
        string = self.__file.readline().strip("\n").strip(" ")
        if string == "":
            raise StopIteration
        return string.split(",")

    def __get_names(self, columns):
        names = []
        for column in columns:
            names.append(column.split("=")[0])
        return names

    def __get_numpy_type(self, ):
        types = []
        for name in self.__column_names:
            types.append((str(name), "f8"))
        return types

    def next(self):
        columns = self.__get_columns()
        final = self.__get_numpy_array()
        return self.__process_row(final, columns)

    def __get_numpy_array(self):
        return numpy.zeros(1, dtype=self.__numpy_type)

    def __process_row(self, final, columns):
        for column in columns:
            value = numpy.float64(column.split("=")[1])
            name = column.split("=")[0]
            final[name] = value
        return final

    def get_event_count(self):
        return self.__event_count

    def close(self):
        self.__file.close()


class EVILWriter(data_loaders.Writer):

    def __init__(self, file_location):
        self.__file = open(file_location, "w")
        self.__line = None
        self.__column_names = None

    def write(self, data):
        # type: (numpy.ndarray) -> None
        self.__line = ""
        self.__setup_writer(data)
        self.__process_row(data)
        self.__line += "\n"
        self.__file.write(self.__line)

    def __setup_writer(self, data):
        # type: (numpy.ndarray) -> None
        if not self.__column_names:
            self.__column_names = data.dtype.names

    def __process_row(self, data):
        # type: (numpy.ndarray) -> None
        for column_index, column in enumerate(self.__column_names):
            self.__append_comma(column_index)
            self.__append_column(column, data)

    def __append_comma(self, column_index):
        # type: (int) -> None
        if column_index > 0:
            self.__line += ","

    def __append_column(self, column_name, data):
        # type: (str, numpy.ndarray) -> None
        string_data = repr(numpy.float64(data[column_name]))
        self.__line += "%s=%s" % (column_name, string_data)

    def close(self):
        self.__file.close()
