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
import numpy as npy
from typing import List

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs.file import misc
from PyPWA.libs.file.processor import data_templates

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


HEADER_SEARCH_BITS = 8192


class SvReader(data_templates.Reader):

    def __init__(self, filename: Path, precision: npy.floating):
        self.__event_count: int = None
        self.__args = (filename, precision)
        self.__file_handle = open(str(filename))
        self.__reader = self.__get_reader()
        self.__elements = next(self.__reader)  # First call is header
        self.__array = self.__get_data_array(precision)

    def __repr__(self) -> str:
        return "{0}({1}, {2})".format(
            self.__class__.__name__, self.__args[0], self.__args[1]
        )

    def __get_reader(self) -> csv.DictReader:
        search_bits = self.__file_handle.read(HEADER_SEARCH_BITS)
        dialect = csv.Sniffer().sniff(search_bits, delimiters=[",", "\t"])
        self.__file_handle.seek(0)
        reader = csv.reader(self.__file_handle, dialect)
        return reader

    def __get_data_array(self, precision: npy.floating):
        array_type = [(name, precision) for name in self.__elements]
        return npy.zeros(1, array_type)

    def next(self) -> npy.ndarray:
        values = next(self.__reader)
        for column_index, element in enumerate(self.__elements):
            self.__array[0][element] = values[column_index]
        return self.__array

    def get_event_count(self) -> int:
        if not self.__event_count:
            length = misc.get_file_length(self.__args[0])
            self.__event_count = length - 1  # Exclude header
        return self.__event_count

    def reset(self):
        self.__file_handle.seek(0)

    def close(self):
        self.__file_handle.close()

    @property
    def fields(self):
        return [name for name in self.__array.dtype.names]


class _SvParser:

    def __repr__(self) -> str:
        return "{0}()".format(self.__class__.__name__)

    def parse(self, filename: Path, precision: npy.floating) -> npy.ndarray:
        data_array = self.__get_array(filename, precision)
        with SvReader(filename, precision) as reader:
            for index, event in enumerate(reader):
                data_array[index] = event
        return data_array

    @staticmethod
    def __get_array(filename: Path, precision: npy.floating) -> npy.ndarray:
        with SvReader(filename, precision) as reader:
            event = reader.next()
        return npy.zeros(reader.get_event_count(), event.dtype)


class SvWriter(data_templates.Writer):

    def __init__(self, filename: Path):
        self.__filename = filename
        self.__file_handle = open(str(filename), "w")
        self.__dialect = self.__get_dialect(filename)
        self.__writer: csv.DictWriter = None
        self.__field_names: List[str] = None

    def __repr__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, self.__filename)

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
            self.__file_handle, fieldnames=self.__field_names,
            dialect=self.__dialect
        )
        self.__writer.writeheader()

    def __write_row(self, data: npy.ndarray):
        dict_data = {}
        for field_name in self.__field_names:
            dict_data[field_name] = repr(data[0][field_name])
        self.__writer.writerow(dict_data)

    def close(self):
        self.__file_handle.close()


class SvMemory(data_templates.Memory):

    def __init__(self):
        self.__parser = _SvParser()

    def __repr__(self) -> str:
        return "{0}()".format(self.__class__.__name__)

    def parse(self, filename: Path, precision: npy.floating):
        return self.__parser.parse(filename, precision)

    def write(self, filename: Path, data: npy.ndarray):
        with SvWriter(filename) as writer:
            for event in data:
                writer.write(npy.array([event], dtype=data.dtype))


class SvReadPackage(data_templates.ReadPackage):

    def __init__(self, filename: Path, precision: npy.floating):
        self.__filename = filename
        self.__precision = precision
        self.__reader = SvReader(filename, precision)
        self.__parser = _SvParser()

    def __repr__(self) -> str:
        return "{0}({1!r}, {2})".format(
            self.__class__.__name__, self.__filename, self.__precision
        )

    def get_reader(self) -> SvReader:
        return self.__reader

    def parse(self) -> npy.ndarray:
        return self.__parser.parse(self.__filename, self.__precision)

    def get_bytes(self) -> int:
        with SvReader(self.__filename, self.__precision) as reader:
            num_cols = len(reader.next().dtype.names)
            num_events = reader.get_event_count()
            num_bytes = self.__precision().nbytes
        return num_cols * num_bytes * num_events

    def get_event_count(self) -> int:
        return self.__reader.get_event_count()
