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

import numpy
from typing import Dict, List, Tuple
from PyPWA import AUTHOR, VERSION
from PyPWA.libs.interfaces import data_loaders
from PyPWA.libs.files import line_count

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


HEADER_SEARCH_BITS = 8192


class SvReader(data_loaders.Reader):

    def __init__(self, file_location):
        # type: (str) -> None
        self.__particle_count = line_count.get_file_length(file_location) - 1
        self.__file = io.open(file_location)
        self.__previous_event = None  # type: numpy.ndarray
        self.__reader = False  # type: csv.DictReader
        self.__types = False  # type: List[Tuple[str]]
        self.__elements = False  # type: List[str]
        self.__start_input()

    def __start_input(self):
        dialect = self.__get_dialect()
        self.__set_reader(dialect)
        self.__set_elements()
        self.__set_numpy_types()

    def __get_dialect(self):
        # type: () -> str
        dialect = csv.Sniffer().sniff(
            self.__file.read(HEADER_SEARCH_BITS), delimiters=[",", "\t"]
        )
        self.__file.seek(0)
        return dialect

    def __set_reader(self, dialect):
        # type: (str) -> None
        self.__reader = csv.reader(self.__file, dialect)

    def __set_elements(self):
        self.__elements = next(self.__reader)

    def __set_numpy_types(self):
        self.__types = []
        for element in self.__elements:
            self.__types.append((element, "f8"))

    def get_event_count(self):
        return self.__particle_count

    def close(self):
        self.__file.close()

    def next(self):
        # type: () -> numpy.ndarray
        non_parsed = list(next(self.__reader))
        parsed = numpy.zeros(1, self.__types)

        for index, element in enumerate(self.__elements):
            parsed[element][0] = non_parsed[index]

        self.__previous_event = parsed

        return self.__previous_event


class SvWriter(data_loaders.Writer):

    def __init__(self, file_location):
        # type: (str) ->  None
        self.__file = open(file_location, "w")
        self.__dialect = None  # type: csv.Dialect
        self.__writer = None  # type: csv.DictWriter
        self.__field_names = None  # type: List[str]
        self.__set_dialect(file_location)

    def __set_dialect(self, file_location):
        # type: (str) -> None
        if self.__is_tab(file_location):
            self.__dialect = csv.excel_tab
        else:
            self.__dialect = csv.excel

    def __is_tab(self, file_location):
        # type: (str) -> bool
        return self.__get_extension(file_location) == "tsv"

    @staticmethod
    def __get_extension(file_location):
        # type: (str) -> str
        return file_location.split(".")[-1]

    def write(self, data):
        # type: (numpy.ndarray) -> None
        self.__writer_setup(data)
        converted_data = self.__convert_to_dict(data)
        self.__write_row(converted_data)

    def __writer_setup(self, data):
        # type: (numpy.ndarray) -> None
        if not self.__writer:
            self.__set_field_names(data)
            self.__set_writer()
            self.__write_header()

    def __set_field_names(self, data):
        # type: (numpy.ndarray) -> None
        self.__field_names = list(data.dtype.names)

    def __set_writer(self):
        self.__writer = csv.DictWriter(
            self.__file,
            fieldnames=self.__field_names,
            dialect=self.__dialect
        )

    def __write_header(self):
        self.__writer.writeheader()

    def __convert_to_dict(self, data):
        # type: (numpy.ndarray) -> Dict[str, str]
        dict_data = {}
        for field_name in self.__field_names:
            dict_data[field_name] = repr(data[0][field_name])
        return dict_data

    def __write_row(self, dict_data):
        # type: (Dict[str, str]) -> None
        self.__writer.writerow(dict_data)

    def close(self):
        self.__file.close()
