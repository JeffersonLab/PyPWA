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

import csv
import io
import logging
import os
import sys
from typing import List, Tuple, Iterable, Dict

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import data_templates

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


HEADER_SEARCH_BITS = 3072


class SvMemory(data_templates.TemplateMemory):

    def parse(self, file_location):
        # type: (str) -> numpy.ndarray
        parser = _SvParser()
        return parser.return_read_data(file_location)

    def write(self, file_location, data):
        # type: (str, numpy.ndarray) -> None
        writer = _SvMemoryWriter()
        writer.write_memory_to_disk(file_location, data)


class _SvParser(object):

    __LOGGER = logging.getLogger(__name__ + "._SvParser")

    def __init__(self):
        self.__line_count = 0
        self.__dialect = None  # type: str
        self.__stream = None  # type: io.FileIO
        self.__reader = None  # type: csv.reader
        self.__header = None  # type: List[str]

    def return_read_data(self, file_location):
        # type: (str) -> numpy.ndarray
        self.__start_parsing(file_location)
        return self.__end_parsing()

    def __start_parsing(self, file_location):
        # type: (str) -> None
        self.__open_stream(file_location)
        self.__set_required_data()

    def __open_stream(self, file_location):
        # type: (str) -> None
        self.__stream = io.open(file_location, "r")

    def __reset_stream(self):
        self.__stream.seek(0)

    def __close_stream(self):
        self.__stream.close()

    def __set_required_data(self):
        self.__set_line_number()
        self.__set_dialect()
        self.__set_reader()
        self.__set_header()

    def __set_line_number(self):
        for self.__line_count, throw_away in enumerate(self.__stream):
            pass
        self.__reset_stream()

    def __set_dialect(self):
        self.__dialect = csv.Sniffer().sniff(
            self.__stream.read(HEADER_SEARCH_BITS), delimiters=[",", "\t"]
        )
        self.__reset_stream()

    def __set_reader(self):
        self.__reader = csv.reader(self.__stream, self.__dialect)

    def __set_header(self):
        self.__header = next(self.__reader)

    def __end_parsing(self):
        # type: () -> numpy.ndarray
        data = self.__parse_data()
        self.__close_stream()
        return data

    def __parse_data(self):
        # type: () -> numpy.ndarray
        empty_array = self.__setup_numpy_array()
        return self.__fill_array(empty_array)

    def __setup_numpy_array(self):
        # type: () -> numpy.ndarray
        types = self.__build_numpy_types()
        return self.__make_empty_numpy_array(types)

    def __build_numpy_types(self):
        # type: () -> List[Tuple[str]]
        types = []
        for column in self.__header:
            types.append((column, "f8"))

        self.__LOGGER.debug("Types: " + repr(types))
        return types

    def __make_empty_numpy_array(self, data_types):
        # type: (List[Tuple[str]]) -> numpy.ndarray
        return numpy.zeros(self.__line_count, data_types)

    def __fill_array(self, empty_array):
        # type: (numpy.ndarray) -> numpy.ndarray
        for row_index, row_data in enumerate(self.__reader):
            # this works because numpy arrays are passed around by reference
            self.__fill_row(empty_array, row_index, row_data)
        return empty_array

    def __fill_row(self, array, row_index, row_data):
        # type: (numpy.ndarray, int, List[str]) -> None
        for column_index in range(len(row_data)):
            array[self.__header[column_index]][row_index] = \
                row_data[column_index]


class _SvMemoryWriter(object):

    def __init__(self):
        self.__dialect = ""  # type: str
        self.__column_names = None  # type: List[str]
        self.__stream = None  # type: io.FileIO
        self.__writer = None  # type: csv.DictWriter

    def write_memory_to_disk(self, file_location, data):
        # type: (str, numpy.ndarray) -> None
        self.__setup_initial_information(file_location, data)
        self.__setup_writer(file_location)
        self.__write_data(data)

    def __setup_initial_information(self, file_location, data):
        # type: (str, numpy.ndarray) -> None
        self.__process_dialect(file_location)
        self.__set_column_names(data)

    def __process_dialect(self, file_location):
        # type: (str) -> None
        extension = self.__get_extension(file_location)
        self.__set_dialect(extension)

    @staticmethod
    def __get_extension(file_location):
        # type: (str) -> str
        return os.path.splitext(file_location)[1]

    def __set_dialect(self, extension):
        # type: (str) -> None
        if extension == ".tsv":
            self.__dialect = csv.excel_tab
        else:
            self.__dialect = csv.excel

    def __set_column_names(self, data):
        # type: (numpy.ndarray) -> None
        self.__column_names = data.dtype.names

    def __setup_writer(self, file_location):
        # type: (str) -> None
        self.__open_stream(file_location)
        self.__set_writer()
        self.__write_header()

    def __open_stream(self, file_location):
        # type: (str) -> None
        if sys.version_info.major == 2:
            self.__stream = open(file_location, "w")
        else:
            self.__stream = io.open(file_location, "w")

    def __set_writer(self):
        self.__writer = csv.DictWriter(
            self.__stream, fieldnames=self.__column_names,
            dialect=self.__dialect
        )

    def __write_header(self):
        self.__writer.writeheader()

    def __write_data(self, data):
        # type: (numpy.ndarray) -> None
        for index in self.__iterator_over_columns(data):
            new_dict = self.__convert_row_to_dict(index, data)
            self.__writer.writerow(new_dict)

    def __iterator_over_columns(self, data):
        # type: (numpy.ndarray) -> Iterable
        length = len(data[self.__column_names[0]])
        return range(length)

    def __convert_row_to_dict(self, row_index, data):
        # type: (int, numpy.ndarray) -> Dict[str, str]
        new_dict = {}
        for column in self.__column_names:
            new_dict[column] = repr(data[column][row_index])
        return new_dict
