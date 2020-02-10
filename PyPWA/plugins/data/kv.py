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

from pathlib import Path
from typing import List, Union

import numpy as npy
import pandas

from PyPWA import info as _info
from PyPWA.libs.file import misc
from PyPWA.libs.file.processor import templates, DataType

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class _EVILDataPlugin(templates.IDataPlugin):

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @property
    def plugin_name(self):
        return "EVIL"

    def get_memory_parser(self):
        return _EVILMemory()

    def get_reader(self, filename):
        return _EVILReader(filename)

    def get_writer(self, filename):
        return _EVILWriter(filename)

    def get_read_test(self):
        return _EVILDataTest()

    @property
    def supported_extensions(self):
        return [".txt", ".kvars"]

    @property
    def supported_data_types(self):
        return [DataType.STRUCTURED]


metadata = _EVILDataPlugin()


class _EVILDataTest(templates.IReadTest):

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def can_read(self, file_location: Path) -> bool:
        try:
            with file_location.open() as stream:
                line = stream.readline()
                equal_count = line.count("=")
                comma_count = line.count(",") + 1
            return equal_count == comma_count and equal_count
        except Exception:
            return False


class _EVILReader(templates.ReaderBase):

    def __init__(self, filename: Path, output_array=False):
        self.__output_array = output_array
        self.__num_event: int = None
        self.__filename = filename
        self.__file_handle = filename.open()
        self.__numpy_array = self.__get_numpy_array()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__filename})"

    def __get_numpy_array(self) -> npy.ndarray:
        names = [column.split("=")[0] for column in self.__get_columns()]
        types = [(str(name), "f8") for name in names]
        self.__file_handle.seek(0)
        return npy.zeros(1, types)

    def next(self) -> Union[pandas.Series, npy.ndarray]:
        for column in self.__get_columns():
            name, value = column.split("=")
            self.__numpy_array[name] = value

        if self.__output_array:
            return self.__numpy_array
        else:
            # If you don't copy the Series will break next call
            return pandas.DataFrame(self.__numpy_array.copy()).loc[0]

    def __get_columns(self) -> List[str]:
        string = self.__file_handle.readline().strip("\n").strip(" ")
        if string == "":
            raise StopIteration
        return string.split(",")

    def get_event_count(self) -> int:
        if not self.__num_event:
            self.__num_event = misc.get_file_length(self.__filename)
        return self.__num_event

    def reset(self):
        self.__file_handle.seek(0)

    def close(self):
        self.__file_handle.close()

    @property
    def fields(self):
        return [name for name in self.__numpy_array.dtype.names]

    @property
    def data_type(self) -> DataType:
        return DataType.STRUCTURED

    @property
    def input_path(self) -> Path:
        return self.__filename


class _EVILWriter(templates.WriterBase):

    def __init__(self, filename: Path):
        self.__column_names: List[str] = None
        self.__filename = filename
        self.__file_handle = filename.open("w")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__filename})"

    def write(self, data: pandas.DataFrame):
        self.__error_check(data)
        line = self.__get_line(data)
        self.__file_handle.write(line)

    def __error_check(self, data: pandas.DataFrame):
        if not self.__column_names:
            self.__column_names = list(data.keys())

    def __get_line(self, data: pandas.DataFrame) -> str:
        line = ""
        for column_index, column in enumerate(self.__column_names):
            line += "," if column_index > 0 else ""
            line += "%s=%.20f" % (column, data[column])
        return line + "\n"

    def close(self):
        self.__file_handle.close()

    @property
    def output_path(self) -> Path:
        return self.__filename


class _EVILMemory(templates.IMemory):

    def __init__(self):
        super(_EVILMemory, self).__init__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def parse(self, filename: Path) -> pandas.DataFrame:
        with _EVILReader(filename, True) as reader:
            data = self.__get_empty_array(filename, len(reader))
            for index, event in enumerate(reader):
                data[index] = event
        return pandas.DataFrame(data)

    @staticmethod
    def __get_empty_array(filename: Path, array_length: int) -> npy.ndarray:
        with filename.open() as stream:
            split = stream.readline().split(",")
            types = [(column.split("=")[0], "f8") for column in split]
        return npy.zeros(array_length, types)

    def write(self, filename: Path, data: pandas.DataFrame):
        with _EVILWriter(filename) as iterator:
            for index, event in data.iterrows():
                iterator.write(event)
