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
from typing import Union

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs.file.processor import data_templates

__credits__ = ["Christopher Banks", "Keandre Palmer", "Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class NumpyReader(data_templates.Reader):

    def __init__(self, filename: Path, data_type: npy.ndarray):
        self.__args = (filename, data_type)
        self.__array = npy.load(str(filename))
        self.__counter = 0

    def __repr__(self) -> str:
        return "{0}({1}, {2})".format(
            self.__class__.__name__, self.__args[0], self.__args[1]
        )

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


class _NumpyParser:

    def __repr__(self) -> str:
        return "{0}()".format(self.__class__.__name__)

    def parse(self, filename: Path, data_type: npy.floating) -> npy.ndarray:
        try:
            return npy.load(str(filename))
        except Exception:
            return self.___load_text(filename, data_type)

    @staticmethod
    def ___load_text(filename: Path, data_type: npy.floating) -> npy.ndarray:
        if filename.suffix == ".pf":
            return npy.loadtxt(str(filename), dtype=bool)
        else:
            return npy.loadtxt(str(filename), dtype=data_type)


class NumpyWriter(data_templates.Writer):

    def __init__(self, filename: Path):
        self.__array = False  # type: Union[npy.ndarray, bool]
        self.__filename = filename

    def __repr__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, self.__filename)

    def write(self, data: npy.void):
        if not isinstance(self.__array, npy.ndarray):
            self.__array = npy.zeros(1, dtype=data.dtype)
            self.__array[0] = data
        else:
            self.__array = npy.resize(self.__array, self.__array.size + 1)
            self.__array[-1] = data

    def close(self):
        npy.save(str(self.__filename), self.__array)


class _NumpyMemoryDump:

    def __repr__(self) -> str:
        return "{0}()".format(self.__class__.__name__)

    def write(self, filename: Path, data: npy.ndarray):
        if filename.suffix == '.npy':
            npy.save(str(filename), data)
        elif filename.suffix == ".pf":
            npy.savetxt(str(filename), data, fmt="%d")
        elif filename.suffix == ".txt":
            npy.savetxt(str(filename), data)
        else:
            npy.save(str(filename), data)


class NumpyMemory(data_templates.Memory):

    def __init__(self):
        self.__parser = _NumpyParser()
        self.__writer = _NumpyMemoryDump()

    def __repr__(self) -> str:
        return "{0}()".format(self.__class__.__name__)

    def parse(self, filename: Path, data_type: npy.floating) -> npy.ndarray:
        return self.__parser.parse(filename, data_type)

    def write(self, filename: Path, data: npy.ndarray):
        self.__writer.write(filename, data)


class NumpyReadPackage(data_templates.ReadPackage):

    def __init__(self, filename: Path, data_type: npy.floating):
        self.__filename = filename
        self.__data_type = data_type
        self.__reader = NumpyReader(filename, data_type)
        self.__array = _NumpyParser().parse(filename, data_type)

    def __repr__(self) -> str:
        return "{0}({1!r}, {2})".format(
            self.__class__.__name__, self.__filename, self.__data_type
        )

    def get_reader(self) -> NumpyReader:
        return self.__reader

    def parse(self) -> npy.ndarray:
        return self.__array

    def get_bytes(self) -> int:
        return self.__array.nbytes

    def get_event_count(self) -> int:
        return len(self.__array)
