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

import os
import numpy

from typing import Union
from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import data_templates

__credits__ = ["Christopher Banks"]
__author__ = AUTHOR
__version__ = VERSION


class _NumpyParser(object):

    def return_read_data(self, file_path):
        # type: (str) -> file_path
        return self.__parsing(file_path)

    def __parsing(self, file_path):
        try:
            return self.__try_parsing_arrays(file_path)
        except Exception:
            return self.__text_file_defined(file_path)

    def __try_parsing_arrays(self, file_path):
        ext = self.__get_extension(file_path)
        if ext == ".npz":
            return self.__multiple_arrays_defined(file_path)
        return self.__single_array_defined(file_path)

    @staticmethod
    def __get_extension(file_path):
        # type: (str) -> file_path
        return os.path.splitext(file_path)[1]

    @staticmethod
    def __multiple_arrays_defined(file_path):
        # type: (Union[str, numpy.ndarray])-> list_of_data
        list_of_data = []
        with numpy.load(file_path) as data:
            for file in data.files:
                list_of_data.append(data[file])
        return numpy.asarray(list_of_data)

    @staticmethod
    def __single_array_defined(file_path):
        # type: (numpy.ndarray)-> data
        data = numpy.load(file_path)
        return data

    def __text_file_defined(self, file_path):
        # type: (str, numpy.ndarray) -> data
        if self.__get_extension(file_path) == ".pf":
            data = numpy.loadtxt(file_path, dtype=bool)
        else:
            data = numpy.loadtxt(file_path)
        return data


class _NumpyMemoryWriter(object):

    def write_memory_to_disk(self, file_path, data):
        # type: (str, numpy.ndarray)-> None
        self.__write_data(file_path, data)

    def __write_data(self, file_path, data):
        # type: (str, numpy.ndarray) -> None
        ext = self.__get_extension(file_path)
        if ext == '.npy':
            numpy.save(file_path, data)
        elif ext == '.npz':
            self.__for_several_arrays(file_path, data)
        elif ext == ".pf":
            numpy.savetxt(file_path, data, fmt="%d")
        elif ext == ".txt":
            numpy.savetxt(file_path, data)
        else:
            numpy.save(file_path, data)

    @staticmethod
    def __get_extension(file_path):
        # type: (str) -> file_path
        return os.path.splitext(file_path)[1]

    @staticmethod
    def __for_several_arrays(file_path, data):
        # type: (str, numpy.ndarray) -> None
        numpy.savez(file_path, *data)


class NumpyMemory(data_templates.TemplateMemory):

    def parse(self, file_location):
        # type: (str) -> file_location
        parser = _NumpyParser()
        return parser.return_read_data(file_location)

    def write(self, file_location, data):
        # type: (str, numpy.ndarray) -> None
        writer = _NumpyMemoryWriter()
        writer.write_memory_to_disk(file_location, data)
