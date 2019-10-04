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
import os
from pathlib import Path
from typing import List

import numpy as npy

from PyPWA.libs.file import misc
from PyPWA.libs.file.processor import templates, DataType
from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


HEADER_SEARCH_BITS = 8192


class _SvDataPlugin(templates.IDataPlugin):

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @property
    def plugin_name(self):
        return "Delimiter Separated Variable sheets"

    def get_memory_parser(self):
        return _SvMemory()

    def get_reader(self, file_location):
        return _SvReader(file_location)

    def get_writer(self, file_location):
        return _SvWriter(file_location)

    def get_read_test(self):
        return _SvDataTest()

    @property
    def supported_extensions(self):
        return [".tsv", ".csv"]

    @property
    def supported_data_types(self):
        return [DataType.STRUCTURED]


metadata = _SvDataPlugin()


class _SvDataTest(templates.IReadTest):

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def can_read(self, filename: Path) -> bool:
        sniffer = csv.Sniffer()
        sniffer.preferred = ['\t', ',']

        try:
            with filename.open() as stream:
                sample = stream.read(HEADER_SEARCH_BITS)
                return sniffer.has_header(sample)
        except Exception:
            return False


class _SvReader(templates.ReaderBase):

    def __init__(self, filename: Path):
        self.__event_count: int = 0
        self.__filename = filename
        self.__file_handle = open(str(filename), "r")
        self.__reader = self.__get_reader()
        self.__elements = next(self.__reader)  # First call is header
        self.__array = self.__get_data_array()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__filename})"

    def __get_reader(self) -> csv.DictReader:
        search_bits = self.__file_handle.read(HEADER_SEARCH_BITS)
        dialect = csv.Sniffer().sniff(search_bits, delimiters=[",", "\t"])
        self.__file_handle.seek(0)
        reader = csv.reader(self.__file_handle, dialect)
        return reader

    def __get_data_array(self):
        array_type = [(name, "f8") for name in self.__elements]
        return npy.zeros(1, array_type)

    def next(self) -> npy.ndarray:
        values = next(self.__reader)
        if not len(values):
            raise StopIteration

        for column_index, element in enumerate(self.__elements):
            self.__array[0][element] = values[column_index]

        return self.__array

    def get_event_count(self) -> int:
        if not self.__event_count:
            length = misc.get_file_length(self.__filename)
            self.__event_count = length - 1  # Exclude header
        return self.__event_count

    def reset(self):
        self.__file_handle.seek(0)
        self.__reader = self.__get_reader()

    def close(self):
        self.__file_handle.close()

    @property
    def fields(self):
        return [name for name in self.__array.dtype.names]

    @property
    def data_type(self) -> DataType:
        return DataType.STRUCTURED

    @property
    def input_path(self) -> Path:
        self.__filename


class _SvWriter(templates.WriterBase):

    def __init__(self, filename: Path):
        self.__filename = filename
        self.__file_handle = open(str(filename), "w")
        self.__dialect = self.__get_dialect(filename)
        self.__writer: csv.DictWriter = None
        self.__field_names: List[str] = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__filename})"

    @staticmethod
    def __get_dialect(file_location: Path) -> csv.Dialect:
        if file_location.suffix == ".tsv":
            return csv.excel_tab
        else:
            return csv.excel

    def write(self, data: npy.ndarray):
        if not self.__writer:
            self.__setup_writer(data)
        self.__write_row(data)

    def __setup_writer(self, data: npy.ndarray):
        self.__field_names = list(data.dtype.names)
        self.__writer = csv.DictWriter(
            self.__file_handle,
            fieldnames=self.__field_names,
            dialect=self.__dialect,
            lineterminator=os.linesep  # Fix issue where \r\n is used on Linux
        )
        self.__writer.writeheader()

    def __write_row(self, data: npy.ndarray):
        dict_data = {}
        for field_name in self.__field_names:
            dict_data[field_name] = repr(data[0][field_name])
        self.__writer.writerow(dict_data)

    def close(self):
        self.__file_handle.close()

    @property
    def output_path(self) -> Path:
        return self.__filename


class _SvMemory(templates.IMemory):

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def parse(self, filename: Path) -> npy.ndarray:
        data_array = self.__get_array(filename)
        with _SvReader(filename) as reader:
            for index, event in enumerate(reader):
                data_array[index] = event
        return data_array

    @staticmethod
    def __get_array(filename: Path) -> npy.ndarray:
        with _SvReader(filename) as reader:
            event = reader.next()
        return npy.zeros(reader.get_event_count(), event.dtype)

    def write(self, filename: Path, data: npy.ndarray):
        with _SvWriter(filename) as writer:
            for event in data:
                writer.write(npy.array([event], dtype=data.dtype))
