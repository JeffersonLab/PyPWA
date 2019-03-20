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

EVIL, Expanded Variable Identification Lists, earned their name from their
inefficient nature when it comes to reading in, writing out, or simply
existing, its a name given to these EVIL formats out of a mixture of spite
and love by current and former developers alike.

This format exists currently only as backwards compatibility, and may not
be bug free or entirely optimized, and may never be. If you are a user
trying to figure out what you should export your data to, or a developer
trying to learn the nature of data within PyPWA, you should move your
attention to CSV/TSV in the SV object and forget that this ever existed.
"""

from PyPWA import AUTHOR, VERSION, Path
from PyPWA.libs.file.processor import data_templates, DataType
from PyPWA.plugins.data.kv import k_process

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _EVILDataTest(data_templates.ReadTest):

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

    def can_read(self, file_location):
        # type: (Path) -> bool
        with file_location.open() as stream:
            line = stream.readline()
            equal_count = line.count("=")
            comma_count = line.count(",") + 1
        return equal_count == comma_count and equal_count


class EVILDataPlugin(data_templates.DataPlugin):

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

    @property
    def plugin_name(self):
        return "EVIL"

    def get_memory_parser(self):
        return k_process.EVILMemory()

    def get_read_package(self, filename, precision):
        return k_process.EVILReadPackage(filename, precision)

    def get_reader(self, filename, precision):
        return k_process.EVILReader(filename, precision)

    def get_writer(self, filename):
        return k_process.EVILWriter(filename)

    def get_read_test(self):
        return _EVILDataTest()

    @property
    def supported_extensions(self):
        return [".txt", ".kvars"]

    @property
    def supported_data_types(self):
        return [DataType.STRUCTURED]
