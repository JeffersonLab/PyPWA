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

from PyPWA import AUTHOR, VERSION, Path
from PyPWA.libs.file.processor import data_templates, DataType
from PyPWA.plugins.data.gamp import g_process

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


_COUNT = 3  # number of events to check


class _GampDataTest(data_templates.ReadTest):

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

    def can_read(self, filename):
        # type: (Path) -> bool
        with filename.open() as stream:
            for i in range(_COUNT):
                line = stream.readline().strip("\n")
                if line == "":
                    if i == 0:
                        return False
                    return True

                try:
                    particle_count = int(line)
                except Exception:
                    return False

                for l in range(particle_count):
                    if len(stream.readline().split(" ")) != 6:
                        return False
        return True


class GampDataPlugin(data_templates.DataPlugin):

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

    @property
    def plugin_name(self):
        return "gamp"

    def get_memory_parser(self):
        return g_process.GampMemory()

    def get_read_package(self, filename, precision):
        return g_process.GampReadPackage(filename, precision)

    def get_writer(self, file_location):
        return g_process.GampWriter(file_location)

    def get_reader(self, file_location, precision):
        return g_process.GampReader(file_location, precision)

    def get_read_test(self):
        return _GampDataTest()

    @property
    def supported_extensions(self):
        return [".gamp"]

    @property
    def supported_data_types(self):
        return [DataType.TREE_VECTOR]
