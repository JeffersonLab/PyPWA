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

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs.file.processor import data_templates, DataType
from . import s_process

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


HEADER_SEARCH_BITS = 8192


class _SvDataTest(data_templates.ReadTest):

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

    def can_read(self, filename):
        # type: (Path) -> bool
        with filename.open() as stream:
            sample = stream.read(HEADER_SEARCH_BITS)
        return self.__has_a_header(sample)

    def __has_a_header(self, sample):
        # type: (str) -> bool
        try:
            self.__get_sniffer().has_header(sample)
            return True
        except Exception:
            return False

    @staticmethod
    def __get_sniffer():
        sniffer = csv.Sniffer()
        sniffer.preferred = ["/t", ","]
        return sniffer


class SvDataPlugin(data_templates.DataPlugin):

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

    @property
    def plugin_name(self):
        return "Delimiter Separated Variable sheets"

    def get_memory_parser(self):
        return s_process.SvMemory()

    def get_reader(self, file_location, precision):
        return s_process.SvReader(file_location, precision)

    def get_read_package(self, filename, precision):
        return s_process.SvReadPackage(filename, precision)

    def get_writer(self, file_location):
        return s_process.SvWriter(file_location)

    def get_read_test(self):
        return _SvDataTest()

    @property
    def supported_extensions(self):
        return [".tsv", ".csv"]

    @property
    def supported_data_types(self):
        return [DataType.STRUCTURED]

