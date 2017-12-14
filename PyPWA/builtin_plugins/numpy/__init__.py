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
from PyPWA.builtin_plugins.numpy import n_memory
from PyPWA.builtin_plugins.numpy import n_read_tests
from PyPWA.builtin_plugins.numpy import n_iterator

__credits__ = ["Christopher Banks", "Keandre Palmer"]
__author__ = AUTHOR
__version__ = VERSION


class NumPyDataPlugin(data_templates.DataPlugin):

    @property
    def plugin_name(self):
        return "NumPy Data Files"

    def get_plugin_memory_parser(self):
        return n_memory.NumpyMemory()

    def get_plugin_reader(self, file_location):
        return n_iterator.NumpyReader(file_location)

    def get_plugin_writer(self, file_location):
        return n_iterator.NumpyWriter(file_location)

    def get_plugin_read_test(self):
        return n_read_tests.NumpyDataTest()

    @property
    def plugin_supported_extensions(self):
        return [".npy", ".pf", ".txt"]

    @property
    def plugin_supports_single_array(self):
        return True

    @property
    def plugin_supports_columned_data(self):
        return True

    @property
    def plugin_supports_tree_data(self):
        return False
