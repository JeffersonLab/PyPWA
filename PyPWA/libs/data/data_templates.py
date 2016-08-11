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

    def __init__(self, thorough=False):
        """
        Simple Data Template, needs to be extended for data plugins.

        Args:
            thorough (bool): Determines if the entire file should be
                validated.
        """
        self._thorough = thorough

    def read_test(self, file_location):
        """
        Command that is called to test if the plugin supports the file.

        Args:
            file_location (str): The location of the file.

        Raises:
            exceptions.IncompatibleData: If data isn't compatible than
                this error would be raised.
        """
        raise NotImplementedError

    def plugin_name(self):
        raise NotImplementedError

    def plugin_supported_extensions(self):
        raise NotImplementedError

    def plugin_memory_parser(self):
        raise NotImplementedError

    def plugin_reader(self):
        raise NotImplementedError

    def plugin_writer(self):
        raise NotImplementedError

    def plugin_supported_length(self):
        return 1


class TemplateMemory(object):

    def parse(self, file_location):
        raise NotImplementedError(
            "%s does not overwrite method parse. This is the method that "
            "you should overwrite to have the object read data into "
            "memory from disk." % self.__class__.__name__
        )

    def write(self, file_location, data):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object write your data to "
            "disk from memory" % self.__class__.__name__
        )
