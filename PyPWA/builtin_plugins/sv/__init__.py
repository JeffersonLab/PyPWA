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

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.components.data_processor import data_templates
from PyPWA.builtin_plugins.sv import s_iterator
from PyPWA.builtin_plugins.sv import s_memory
from PyPWA.builtin_plugins.sv import s_read_tests

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class SvDataPlugin(data_templates.DataPlugin):

    @property
    def plugin_name(self):
        return "Delimiter Separated Variable sheets"

    def get_plugin_memory_parser(self):
        return s_memory.SvMemory()

    def get_plugin_reader(self, file_location):
        return s_iterator.SvReader(file_location)

    def get_plugin_writer(self, file_location):
        return s_iterator.SvWriter(file_location)

    def get_plugin_read_test(self):
        return s_read_tests.SvDataTest()

    @property
    def plugin_supported_extensions(self):
        return [".tsv", ".csv"]

    @property
    def plugin_supports_columned_data(self):
        return True

    @property
    def plugin_supports_particle_pool(self):
        return False

    @property
    def plugin_supports_single_array(self):
        return False
