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
Main object for iterating over data.
"""

import logging
import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.data_handler import _plugin_finder
from PyPWA.libs.data_handler import exceptions
from PyPWA.libs.data_handler import data_templates

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Iterator(object):

    __LOGGER = logging.getLogger(__name__ + ".Iterator")

    def __init__(self, fail=True, user_plugin=""):
        # type: (bool, str) -> None
        self.__fail = fail
        self.__plugin_fetcher = _plugin_finder.PluginSearch(user_plugin)

    def return_reader(self, file_location):
        # type: (str) -> data_templates.Reader
        try:
            return self.__get_reader_plugin(file_location)
        except exceptions.UnknownData as Error:
            self.__error_management(Error)

    def __get_reader_plugin(self, file_location):
        # type: (str) -> data_templates.Reader
        plugin = self.__plugin_fetcher.get_read_plugin(file_location)
        return plugin.get_plugin_reader(file_location)

    def return_writer(self, file_location, data):
        # type: (str, numpy.ndarray) -> data_templates.Writer
        try:
            return self.__get_writer_plugin(file_location, data)
        except exceptions.UnknownData as Error:
            self.__error_management(Error)

    def __get_writer_plugin(self, file_location, data):
        # type: (str, numpy.ndarray) -> data_templates.Writer
        plugin = self.__plugin_fetcher.get_write_plugin(file_location, data)
        return plugin.get_plugin_writer(file_location)

    def __error_management(self, error):
        # type: (Exception) -> None
        if self.__fail:
            raise error
