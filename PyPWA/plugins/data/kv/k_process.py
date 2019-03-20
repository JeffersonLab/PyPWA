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

EVIL (Expanded Variable Identification Lists) earned their name from their
inefficient nature when it comes to reading in, writing out, or simply
existing, its a name given to these EVIL formats out of a mixture of spite
and love by current and former developers alike.

This format exists currently only as backwards compatibility, and may not
be bug free or entirely optimized, and may never be. If you are a user
trying to figure out what you should export your data to, or a developer
trying to learn the nature of data within PyPWA, you should move your
attention to CSV/TSV in the SV object and forget that this ever existed.
"""

import numpy as npy
from typing import List

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs.file import misc
from PyPWA.libs.file.processor import data_templates

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class EVILReader(data_templates.Reader):

    def __init__(self, filename: Path, precision: npy.floating):
        self.__num_event: int = None
        self.__args = (filename, precision)
        self.__file_handle = filename.open()
        self.__numpy_array = self.__get_numpy_array(precision)

    def __repr__(self) -> str:
        return "{0}({1!r}, {2!r})".format(
            self.__class__.__name__, self.__args[0], self.__args[1]
        )

    def __get_numpy_array(self, precision: npy.dtype) -> npy.ndarray:
        names = [column.split("=")[0] for column in self.__get_columns()]
        types = [(str(name), precision) for name in names]
        self.__file_handle.seek(0)
        return npy.zeros(1, types)

    def next(self) -> npy.ndarray:
        for column in self.__get_columns():
            name, value = column.split("=")
            self.__numpy_array[name] = value
        return self.__numpy_array

    def __get_columns(self) -> List[str]:
        string = self.__file_handle.readline().strip("\n").strip(" ")
        if string == "":
            raise StopIteration
        return string.split(",")

    def get_event_count(self) -> int:
        if not self.__num_event:
            self.__num_event = misc.get_file_length(self.__args[0])
        return self.__num_event

    def reset(self):
        self.__file_handle.seek(0)

    def close(self):
        self.__file_handle.close()

    @property
    def fields(self):
        return [name for name in self.__numpy_array.dtype.names]


class _EVILParser:

    def __repr__(self) -> str:
        return "{0}()".format(self.__class__.__name__)

    def parse(self, filename: Path, precision: npy.floating) -> npy.ndarray:
        with EVILReader(filename, precision) as reader:
            array = self.__get_empty_array(filename, len(reader), precision)
            for index, event in enumerate(reader):
                array[index] = event
        return array

    @staticmethod
    def __get_empty_array(
            filename: Path, array_length: int, precision: npy.floating
    ) -> npy.ndarray:
        with filename.open() as stream:
            split = stream.readline().split(",")
            types = [(column.split("=")[0], precision) for column in split]
        return npy.zeros(array_length, types)


class EVILWriter(data_templates.Writer):

    def __init__(self, filename: Path):
        self.__column_names: List[str] = None
        self.__filename = filename
        self.__file_handle = filename.open("w")

    def __repr__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, self.__filename)

    def write(self, data: npy.ndarray):
        self.__error_check(data)
        line = self.__get_line(data)
        self.__file_handle.write(line)

    def __error_check(self, data: npy.ndarray):
        if not self.__column_names:
            self.__column_names = list(data.dtype.names)

    def __get_line(self, data: npy.ndarray) -> str:
        line = u""
        for column_index, column in enumerate(self.__column_names):
            line += "," if column_index > 0 else ""
            line += "{0}={1}".format(column, data[column])
        return line + "\n"

    def close(self):
        self.__file_handle.close()


class EVILMemory(data_templates.Memory):

    def __init__(self):
        super(EVILMemory, self).__init__()
        self.__parser = _EVILParser()

    def __repr__(self) -> str:
        return "{0}()".format(self.__class__.__name__)

    def parse(self, filename: Path, precision: npy.floating) -> npy.ndarray:
        return self.__parser.parse(filename, precision)

    def write(self, filename: Path, data: npy.ndarray):
        with EVILWriter(filename) as iterator:
            for event in npy.nditer(data):
                iterator.write(event)


class EVILReadPackage(data_templates.ReadPackage):
    
    def __init__(self, filename: Path, precision: npy.floating):
        self.__filename = filename
        self.__precision = precision
        self.__reader = EVILReader(filename, precision)
        self.__parser = _EVILParser()

    def __repr__(self) -> str:
        return "{0}({1!r}, {2})".format(
            self.__class__.__name__, self.__filename, self.__precision
        )

    def get_reader(self) -> EVILReader:
        return self.__reader

    def parse(self) -> npy.ndarray:
        return self.__parser.parse(self.__filename, self.__precision)

    def get_bytes(self):
        with self.__filename.open() as stream:
            num_columns = len(stream.readline().split(","))
            num_events = self.get_event_count()
            num_bytes = self.__precision().nbytes
        return num_columns * num_events * num_bytes

    def get_event_count(self) -> int:
        return self.__reader.get_event_count()
