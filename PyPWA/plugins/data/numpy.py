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

from pathlib import Path
from typing import Union

import numpy as npy
import pandas

from PyPWA import info as _info
from PyPWA.libs.file.processor import templates, DataType

__credits__ = ["Christopher Banks", "Keandre Palmer", "Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


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
        return [".npy", ".pf", ".txt", ".sel", ".bamp"]

    @property
    def supported_data_types(self):
        return [DataType.BASIC, DataType.STRUCTURED]


metadata = _NumpyDataPlugin()


def pandas_to_structured(
        pd: Union[pandas.Series, pandas.DataFrame]) -> npy.ndarray:

    if isinstance(pd, pandas.Series) and isinstance(pd.name, (type(None), str)):
        return pd.to_numpy()

    names = list(pd.keys())
    types = pd.dtypes if len(pd.dtypes) else [pd.dtypes] * len(names)

    array_type = []
    for name, dtype in zip(names, types):
        array_type.append((name, dtype))

    if isinstance(pd, pandas.Series):
        length = 1
    else:
        length = len(pd)

    array = npy.empty(length, array_type)
    for name in names:
        array[name] = pd[name]
    return array


class _NumpyDataTest(templates.IReadTest):

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def can_read(self, filename):
        if self.__can_load_binary(filename) or self.__can_load_text(filename):
            return True
        else:
            return False

    @staticmethod
    def __can_load_binary(file_location: Path) -> bool:
        try:
            npy.load(str(file_location))
            return True
        except Exception:
            return False

    @staticmethod
    def __can_load_text(file_location: Path) -> bool:
        try:
            npy.loadtxt(str(file_location))
            return True
        except Exception:
            return False


class _NumpyReader(templates.ReaderBase):

    def __init__(self, filename: Path):
        self.__filename = filename
        self.__array = self.__load_data()
        self.__counter = 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__filename})"

    def __load_data(self) -> Union[pandas.DataFrame, pandas.Series]:
        data = _NumpyMemory().parse(self.__filename)

        if isinstance(data, npy.ndarray):
            if data.dtype.names:
                return pandas.DataFrame(data)
            else:
                return pandas.Series(data)
        else:
            return data

    def get_event_count(self) -> int:
        return len(self.__array)

    def next(self) -> Union[pandas.Series]:
        if self.__counter < len(self):
            self.__counter += 1
            return self.__array.iloc[self.__counter-1]
        else:
            raise StopIteration

    def reset(self):
        self.__counter = 0

    def close(self):
        del self.__array

    @property
    def fields(self):
        return [name for name in self.__array.dtype.names]

    @property
    def data_type(self) -> DataType:
        if self.__array.dtype.names:
            return DataType.STRUCTURED
        else:
            return DataType.BASIC

    @property
    def input_path(self) -> Path:
        return self.__filename


class _NumpyWriter(templates.WriterBase):

    def __init__(self, filename: Path):
        self.__array: npy.ndarray = False
        self.__filename = filename

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def write(self, data: npy.void):
        if isinstance(data, (pandas.Series, pandas.DataFrame)):
            data = pandas_to_structured(data)

        if not isinstance(self.__array, npy.ndarray):
            self.__array = npy.zeros(1, dtype=data.dtype)
            self.__array[0] = data
        else:
            self.__array = npy.resize(self.__array, self.__array.size + 1)
            self.__array[-1] = data

    def close(self):
        if self.__filename.suffix == ".txt":
            npy.savetxt(str(self.__filename), self.__array)
        elif self.__filename.suffix in (".pf", ".sel"):
            npy.savetxt(str(self.__filename), self.__array, fmt="%d")
        elif self.__filename.suffix == ".bamp":
            with self.__filename.open("wb") as stream:
                self.__array.tofile(stream)
        else:
            npy.save(str(self.__filename), self.__array)

    @property
    def output_path(self) -> Path:
        return self.__filename


class _NumpyMemory(templates.IMemory):

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def parse(self, filename: Path) -> Union[pandas.DataFrame, pandas.Series]:
        try:
            data = npy.load(str(filename))
            if data.dtype.names:
                return pandas.DataFrame(data)
            else:
                return pandas.Series(data)
        except Exception:
            return pandas.Series(self.___load_text(filename))

    @staticmethod
    def ___load_text(filename: Path) -> npy.ndarray:
        if filename.suffix == ".pf":
            return npy.loadtxt(str(filename), dtype=bool)
        elif filename.suffix == ".sel":
            return npy.loadtxt(str(filename), dtype="u4")
        else:
            return npy.loadtxt(str(filename))

    def write(
            self, filename: Path, data: Union[pandas.DataFrame, pandas.Series]):

        data = pandas_to_structured(data)

        if filename.suffix in (".pf", ".sel"):
            npy.savetxt(str(filename), data, fmt="%d")
        elif filename.suffix == ".bamp":
            with filename.open("wb") as stream:
                data.tofile(stream)
        elif filename.suffix == ".txt":
            npy.savetxt(str(filename), data)
        else:
            npy.save(str(filename), data)
