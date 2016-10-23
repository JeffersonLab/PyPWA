#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Holds Data Exceptions

These exceptions are written to help aid the Data module and improve
readability of the traceback errors without obscuring more complex errors.
"""

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class TemplateDataPlugin(object):

    @property
    def plugin_name(self):
        raise NotImplementedError()

    def get_plugin_memory_parser(self):
        raise NotImplementedError()

    def get_plugin_reader(self):
        raise NotImplementedError()

    def get_plugin_writer(self):
        raise NotImplementedError()

    def get_plugin_read_test(self):
        raise NotImplementedError()

    @property
    def plugin_supported_extensions(self):
        raise NotImplementedError()

    @property
    def plugin_supports_flat_data(self):
        raise NotImplementedError()

    @property
    def plugin_supports_gamp_data(self):
        raise NotImplementedError()


class TemplateMemory(object):
    def parse(self, file_location):
        raise NotImplementedError()

    def write(self, file_location, data):
        raise NotImplementedError()


class ReadTest(object):

    def quick_test(self):
        """
        Raises:
            PyPWA.builtin_plugins.data.exceptions.IncompatibleData: Raised
                when data  failed to test properly for the file.
        """
        raise NotImplementedError()

    def full_test(self):
        """
        Raises:
            PyPWA.builtin_plugins.data.exceptions.IncompatibleData: Raised
                when data  failed to test properly for the file.
        """
        raise NotImplementedError()
