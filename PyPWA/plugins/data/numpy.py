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

import numpy as npy

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs.file.processor import templates, DataType

__credits__ = ["Christopher Banks", "Keandre Palmer", "Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _NumpyDataPlugin(templates.IDataPlugin):

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @property
    def plugin_name(self):
        return "NumPy Data Files"

    def get_memory_parser(self):
        return _NumpyMemory()

    def get_reader(self, filename):
        return _NumpyReader(filename)

    def get_writer(self, filename):
        return _NumpyWriter(filename)

    def get_read_test(self):
        return _NumpyDataTest()

    @property
    def supported_extensions(self):
        return [".npy", ".pf", ".txt"]

    @property
    def supported_data_types(self):
        return [DataType.BASIC, DataType.STRUCTURED]


metadata = _NumpyDataPlugin()


class _NumpyDataTest(templates.IReadTest):

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def can_read(self, filename):
        if self.__can_load_binary(filename) or self.__can_load_text(filename):
            return True
        else:
            return False

    @staticmethod
    def __can_load_binary(file_location):
        # type: (Path) -> bool
        try:
            npy.load(str(file_location))
            return True
        except Exception:
            return False

    @staticmethod
    def __can_load_text(file_location):
        # type: (Path) -> bool
        try:
            npy.loadtxt(str(file_location))
            return True
        except Exception:
            return False


class _NumpyReader(templates.ReaderBase):

    def __init__(self, filename: Path):
        self.__filename = filename
        self.__array = npy.load(str(filename))
        self.__counter = 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__filename})"

    def get_event_count(self) -> int:
        return len(self.__array)

    def next(self) -> npy.ndarray:
        if self.__counter < len(self):
            self.__counter += 1
            return self.__array[self.__counter-1]
        else:
            raise StopIteration

    def reset(self):
        self.__counter = 0

    def close(self):
        del self.__array

    @property
    def fields(self):
        return [name for name in self.__array.dtype.names]


class _NumpyWriter(templates.WriterBase):

    def __init__(self, filename: Path):
        self.__array: npy.ndarray = False
        self.__filename = filename

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def write(self, data: npy.void):
        if not isinstance(self.__array, npy.ndarray):
            self.__array = npy.zeros(1, dtype=data.dtype)
            self.__array[0] = data
        else:
            self.__array = npy.resize(self.__array, self.__array.size + 1)
            self.__array[-1] = data

    def close(self):
        npy.save(str(self.__filename), self.__array)


class _NumpyMemory(templates.IMemory):

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def parse(self, filename: Path) -> npy.ndarray:
        try:
            return npy.load(str(filename))
        except Exception:
            return self.___load_text(filename)

    @staticmethod
    def ___load_text(filename: Path) -> npy.ndarray:
        if filename.suffix == ".pf":
            return npy.loadtxt(str(filename), dtype=bool)
        else:
            return npy.loadtxt(str(filename))

    def write(self, filename: Path, data: npy.ndarray):
        if filename.suffix == '.npy':
            npy.save(str(filename), data)
        elif filename.suffix == ".pf":
            npy.savetxt(str(filename), data, fmt="%d")
        elif filename.suffix == ".txt":
            npy.savetxt(str(filename), data)
        else:
            npy.save(str(filename), data)
