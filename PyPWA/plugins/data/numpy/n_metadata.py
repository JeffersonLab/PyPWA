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

from PyPWA import AUTHOR, VERSION, Path
from PyPWA.libs.file.processor import data_templates, DataType
from . import n_process

__credits__ = ["Christopher Banks", "Keandre Palmer", "Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _NumpyDataTest(data_templates.ReadTest):

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

    def can_read(self, filename):
        if self.__can_load_binary(filename) or self.__can_load_text(filename):
            return True
        else:
            return False

    @staticmethod
    def __can_load_binary(file_location):
        # type: (Path) -> bool
        try:
            numpy.load(str(file_location))
            return True
        except Exception:
            return False

    @staticmethod
    def __can_load_text(file_location):
        # type: (Path) -> bool
        try:
            numpy.loadtxt(str(file_location))
            return True
        except Exception:
            return False


class NumpyDataPlugin(data_templates.DataPlugin):

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

    @property
    def plugin_name(self):
        return "NumPy Data Files"

    def get_memory_parser(self):
        return n_process.NumpyMemory()

    def get_read_package(self, filename, precision):
        return n_process.NumpyReadPackage(filename, precision)

    def get_reader(self, filename, precision):
        return n_process.NumpyReader(filename, precision)

    def get_writer(self, filename):
        return n_process.NumpyWriter(filename)

    def get_read_test(self):
        return _NumpyDataTest()

    @property
    def supported_extensions(self):
        return [".npy", ".pf", ".txt"]

    @property
    def supported_data_types(self):
        return [DataType.BASIC, DataType.STRUCTURED]

