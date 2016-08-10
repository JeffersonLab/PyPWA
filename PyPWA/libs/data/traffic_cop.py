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
The utility objects for the Data Plugin

This holds all the main objects for the data plugin. This has search
functions but these objects should never know anything about the data
plugin they are trying to load, all it should ever care about is that
there is metadata that contains enough information about the plugin for
this to get started passing data to it.
"""

import logging

from PyPWA.configurator import plugin_loader, templates
from PyPWA.libs.data import exceptions
from PyPWA.libs.data import _utilites
from PyPWA.libs.data import builtin
from PyPWA.libs.data import data_templates
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Memory(templates.DataParserTemplate):
    def __init__(
            self, cache=True, clear_cache=False, fail=True,
            user_plugin=False, options=False
    ):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        self._cache = cache
        self._clear_cache = clear_cache
        self._fail = fail
        self._user_plugin = user_plugin

        if options:
            super(Memory, self).__init__(options)

        plugin_finder = plugin_loader.PluginLoading(
            data_templates.TemplateDataPlugin
        )

        data_plugins = plugin_finder.fetch_plugin(
            [builtin, self._user_plugin]
        )

        self._data_search = _utilites.DataSearch(data_plugins)

    def parse(self, text_file):
        """
        Parses a single file into memory then passes that data back to the
        main object.

        Args:
            text_file (str): The non-parsed settings from the
                configuration file.

        Returns:
            The data that was loaded in from file.

        Raises:
            definitions.UnknownData: If the loading of the file fails and
                fail on parse error is set to true then this will be
                raised.
        """
        try:
            plugin = self._data_search.search(text_file)
            parser = plugin.metadata_data["memory"]()
            return parser.parse(text_file)
        except exceptions.UnknownData:
            if self._fail:
                raise
            else:
                return 0

    def write(self, data, text_file):
        """
        Writes data from memory into a file.

        Args:
            data (numpy.ndarray): The data that needs to be
                written to disk.
            text_file (str): The file that needs to be parsed.

        Raises:
            definitions.UnknownData: If the loading of the file fails and
                fail on parse error is set to true then this will be
                raised.
        """
        try:
            plugin = self._data_search.search(text_file)
            parser = plugin.metadata_data["memory"]()
            parser.write(text_file, data)
        except exceptions.UnknownData:
            if self._fail:
                raise


class Iterator(templates.DataReaderTemplate):
    def __init__(self, fail=True, user_plugin=False, options=False):
        """
        The data plugin.

        Args:

        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        self._fail = fail
        self._user_plugin = user_plugin

        if options:
            super(Iterator, self).__init__(options)

        plugin_finder = plugin_loader.PluginLoading(
            data_templates.TemplateDataPlugin
        )

        data_plugins = plugin_finder.fetch_plugin(
            [builtin, self._user_plugin]
        )

        self._data_search = _utilites.DataSearch(data_plugins)

    def return_reader(self, text_file):
        """
        Searches for the correct reader than passes that back to the
        requesting object.

        Args:
            text_file (str): The line that contains the settings.

        Returns:
            object: The reader that was requested.
            bool: False if it failed to find a reader.

        Raises:
            definitions.UnknownData: If the loading of the file fails and
                fail on parse error is set to true then this will be
                raised.
        """
        try:
            plugin = self._data_search.search(text_file)
            reader = plugin.metadata_data["reader"](text_file)
            return reader
        except exceptions.UnknownData:
            if self._fail:
                raise
            else:
                return 0

    def return_writer(self, text_file):
        """
        Searches for the correct writer than passes that back to the
        requesting object.

        Args:
            text_file (str): The line that contains the settings.

        Returns:
            object: The writer that was requested.
            bool: False if it failed to find a writer

        Raises:
            definitions.UnknownData: If the loading of the file fails and
                fail on parse error is set to true then this will be
                raised.
        """
        try:
            plugin = self._data_search.search(text_file)
            writer = plugin.metadata_data["writer"](text_file)
            return writer
        except exceptions.UnknownData:
            if self._fail:
                raise
            else:
                return 0
