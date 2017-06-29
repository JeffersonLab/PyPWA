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

from typing import List, Tuple

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import data_templates
from PyPWA.core.shared import file_libs
from PyPWA.builtin_plugins.data.builtin.kv import k_iterator

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _CreateEmptyArray(object):

    def __init__(self):
        self.__file_location = None
        self.__split = None

    def create_empty_array(self, file_location):
        # type: (str) -> numpy.ndarray
        self.__file_location = file_location
        length = file_libs.get_file_length(file_location)
        self.__get_split_of_first_line()
        names = self.__get_column_names()
        types = self.__create_numpy_type(names)
        return self.__create_array(length, types)

    def __get_split_of_first_line(self):
        with open(self.__file_location) as stream:
            self.__split = stream.readline().split(",")

    def __get_column_names(self):
        # type: () -> List[str]
        names = []
        for name in range(len(self.__split)):
            names.append(self.__split[name].split("=")[0])
        return names

    def __create_numpy_type(self, names):
        # type: (List[str]) -> List[Tuple[str,str]]
        types = []
        for name in names:
            types.append((str(name), "f8"))
        return types

    def __create_array(self, length, types):
        # type: (int, List[Tuple[str, str]]) -> numpy.ndarray
        return numpy.zeros(length, types)


class _EVILParser(object):

    def __init__(self):
        self.__create_empty_array = _CreateEmptyArray()
        self.__array = None  # type: numpy.ndarray

    def parse(self, file_location):
        # type: (str) -> numpy.ndarray
        self.__set_empty_array(file_location)
        self.__process_file(file_location)
        return self.__array

    def __set_empty_array(self, file_location):
        # type: (str) -> None
        self.__array = self.__create_empty_array.create_empty_array(
            file_location
        )

    def __process_file(self, file_location):
        # type: (str) -> None
        with k_iterator.EVILReader(file_location) as iterator:
            for index, event in enumerate(iterator):
                self.__array[index] = event


class _EVILWriter(object):

    def write(self, file_location, data):
        # type: (str, numpy.ndarray) -> None
        with k_iterator.EVILWriter(file_location) as iterator:
            for event in numpy.nditer(data):
                iterator.write(event)


class EVILMemory(data_templates.TemplateMemory):

    def __init__(self):
        super(EVILMemory, self).__init__()
        self.__parser = _EVILParser()
        self.__writer = _EVILWriter()

    def parse(self, file_location):
        return self.__parser.parse(file_location)

    def write(self, file_location, data):
        self.__writer.write(file_location, data)
