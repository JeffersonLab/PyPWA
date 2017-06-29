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

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import data_templates
from PyPWA.builtin_plugins.data.builtin.kv import k_iterator
from PyPWA.builtin_plugins.data.builtin.kv import k_memory
from PyPWA.builtin_plugins.data.builtin.kv import k_read_tests

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class EVILDataPlugin(data_templates.TemplateDataPlugin):

    def __init__(self):
        super(EVILDataPlugin, self).__init__()

    @property
    def plugin_name(self):
        return "EVIL"

    def get_plugin_memory_parser(self):
        return k_memory.EVILMemory()

    def get_plugin_reader(self, file_location):
        return k_iterator.EVILReader(file_location)

    def get_plugin_writer(self, file_location):
        return k_iterator.EVILWriter(file_location)

    def get_plugin_read_test(self):
        return k_read_tests.EVILDataTest()

    @property
    def plugin_supported_extensions(self):
        return [".txt", ".kvars"]

    @property
    def plugin_supports_columned_data(self):
        return True

    @property
    def plugin_supports_single_array(self):
        return False

    @property
    def plugin_supports_tree_data(self):
        return False
