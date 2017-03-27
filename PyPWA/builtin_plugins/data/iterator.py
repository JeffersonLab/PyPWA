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

import logging

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import _plugin_finder
from PyPWA.builtin_plugins.data import exceptions
from PyPWA.core.shared.interfaces import plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Iterator(plugins.DataIterator):

    _logger = logging.getLogger(__name__)
    _fail = True
    _plugin_fetcher = _plugin_finder.PluginSearch

    def __init__(self, fail=True, user_plugin=""):
        self._logger.addHandler(logging.NullHandler())

        self._fail = fail
        self._plugin_fetcher = _plugin_finder.PluginSearch(user_plugin)

    def return_reader(self, file_location):
        try:
            return self._get_reader_plugin(file_location)
        except exceptions.UnknownData as Error:
            self._error_management(Error)

    def _get_reader_plugin(self, file_location):
        plugin = self._plugin_fetcher.get_read_plugin(file_location)
        return plugin.get_plugin_reader(file_location)

    def return_writer(self, file_location, data_shape):
        try:
            self._get_writer_plugin(file_location, data_shape)
        except exceptions.UnknownData as Error:
            self._error_management(Error)

    def _get_writer_plugin(self, file_location, data):
        plugin = self._plugin_fetcher.get_write_plugin(file_location, data)
        return plugin.get_plugin_writer(file_location)

    def _error_management(self, error):
        if self._fail:
            raise error
