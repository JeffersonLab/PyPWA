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

import PyPWA.libs.data
from PyPWA.configurator import settings_aid
from PyPWA.libs.data import definitions
from PyPWA.libs.data import _utilites
from PyPWA.libs.data import builtin
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION

BUILTIN_PACKAGE_LOCATION = builtin.__file__


class TrafficCop(object):

    def parse(self, settings_line):
        """
        Parses a single file into memory then passes that data back to the
        main object.

        Args:
            settings_line (str): The non-parsed settings from the
                configuration file.

        Returns:
            The data that was loaded in from file.

        Raises:
            definitions.UnknownData: If the loading of the file fails and
                fail on parse error is set to true then this will be
                raised.
        """
        try:
            plugin = self._data_search.search(settings_line)
            parser = plugin.metadata_data["memory"]()
            return parser.parse(settings_line)
        except definitions.UnknownData:
            if self._corrected_settings["fail"]:
                raise
            else:
                return 0

    # Going to assume for completions sake that the settings line is just
    def __init__(
            self, cache=False, clear_cache=False, plugins=False,
            settings=False
    ):
        """
        The data plugin.

        Args:
            settings (dict): The global options.
            cache (bool): Whether or not to cache data.
            clear_cache (bool): Should the cache be cleared when called
            plugins (list[str]): The list of directories that the plugins
                should be in.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        plugin_finder = _utilites.FindPlugins()

        if settings:
            fixer = settings_aid.CorrectSettings()
            options = PyPWA.libs.data.Options()
            self._corrected_settings = fixer.correct_dictionary(
                settings, options.return_template)
            data_plugins = plugin_finder.find_plugin(
                [builtin, settings["user plugin"]]
            )

            self._cache = settings["cache"]
            self._clear_cache = settings["clear cache"]

        else:
            data_plugins = plugin_finder.find_plugin(
                [builtin, plugins]
            )
            self._cache = cache
            self._clear_cache = clear_cache

        self._data_search = _utilites.DataSearch(data_plugins)
    # the file's location. However untrue this may be.

    def write(self, file_location, data):
        """
        Writes data from memory into a file.

        Args:
            file_location (str): The file that needs to be parsed.
            data (numpy.ndarray): The data that needs to be
                written to disk.

        Raises:
            definitions.UnknownData: If the loading of the file fails and
                fail on parse error is set to true then this will be
                raised.
        """
        try:
            plugin = self._data_search.search(file_location)
            parser = plugin.metadata_data["memory"]()
            parser.write(file_location, data)
        except definitions.UnknownData:
            if self._corrected_settings["fail"]:
                raise

    def reader(self, settings_line):
        """
        Searches for the correct reader than passes that back to the
        requesting object.

        Args:
            settings_line (str): The line that contains the settings.

        Returns:
            object: The reader that was requested.
            bool: False if it failed to find a reader.

        Raises:
            definitions.UnknownData: If the loading of the file fails and
                fail on parse error is set to true then this will be
                raised.
        """
        try:
            plugin = self._data_search.search(settings_line)
            reader = plugin.metadata_data["reader"](settings_line)
            return reader
        except definitions.UnknownData:
            if self._corrected_settings["fail"]:
                raise
            else:
                return 0

    def writer(self, settings_line):
        """
        Searches for the correct writer than passes that back to the
        requesting object.

        Args:
            settings_line (str): The line that contains the settings.

        Returns:
            object: The writer that was requested.
            bool: False if it failed to find a writer

        Raises:
            definitions.UnknownData: If the loading of the file fails and
                fail on parse error is set to true then this will be
                raised.
        """
        try:
            plugin = self._data_search.search(settings_line)
            writer = plugin.metadata_data["writer"](settings_line)
            return writer
        except definitions.UnknownData:
            if self._corrected_settings["fail"]:
                raise
            else:
                return 0
