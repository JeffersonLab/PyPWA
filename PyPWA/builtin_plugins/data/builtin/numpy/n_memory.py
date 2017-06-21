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

import numpy
from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import data_templates

__credits__ = ["Christopher Banks"]
__author__ = AUTHOR
__version__ = VERSION


class NumpyMemory(data_templates.TemplateMemory):

    def parse(self, file_location):
        # type: (str) -> numpy.ndarray
        parser = _NumpyParser()
        return parser.return_read_data(file_location)

    def write(self, file_location, data):
        # type: (str, numpy.ndarray) -> None
        writer = _NumpyMemoryWriter()
        writer.write_memory_to_disk(file_location, data)


class _NumpyParser(object):

    def return_read_data(self, file_path):
        return self.__parsing(file_path)

    @staticmethod
    def __parsing(file_path):
        # type: (str) -> numpy.ndarray
        try:
            data = numpy.load(file_path)
            return data

        except OSError:
            data = numpy.loadtxt(file_path)
            return data


class _NumpyMemoryWriter(object):

    def write_memory_to_disk(self, file_path, data):
        self.__write_data(file_path, data)

    def __write_data(self, file_path, data):
        # type: (str) -> numpy.ndarray
        ext = self.__get_extension(file_path)
        if ext == '.npy' or '.pf':
            numpy.save(file_path, data)
        elif ext == '.npz':
            if data is dict:
                numpy.savez(file_path, **data)
            else:
                numpy.savez(file_path, *data)

    @staticmethod
    def __get_extension(file_path):
        return file_path.split(".")[-1]

