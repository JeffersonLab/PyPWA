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

import os

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.configurator import plugin_loader
from PyPWA.configurator import templates
from PyPWA.configurator import tools
from PyPWA.libs.data import _cache
from PyPWA.libs.data import builtin
from PyPWA.libs.data import data_templates
from PyPWA.libs.data import exceptions

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


MODULE_NAME = "Builtin Parser"  # Name for the module externally.


class DataCoreTools(object):

    def _search(self, file_location):
        """
        Loops through the objects plugin list until it finds a validator
        that doesn't fail, then returns that plugin.

        Args:
            file_location (str): The location of the file that needs to be
                parsed.

        Returns:
            data_templates.TemplateDataPlugin

        Raises:
            exceptions.UnknownData: If no plugin reports that it can read
                the data then this will be raised to alert the caller that
                the data is unreadable.
        """
        for plugin in self._data_plugins:
            try:
                validator = plugin()

                validator.read_test(file_location)
                self._logger.info("Found %s will load %s" %
                                  (plugin.__name__, file_location))
                return validator
            except exceptions.IncompatibleData:
                self._logger.debug("Skipping %s for data %s" %
                                   (plugin.__name__, file_location))
        raise exceptions.UnknownData(
            "Unable to find a plugin that can load %s" % file_location
        )


class Memory(templates.DataParserTemplate, DataCoreTools):
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
            super(Memory, self).__init__(options=options)

        plugin_finder = plugin_loader.PluginLoading(
            data_templates.TemplateDataPlugin
        )

        data_plugins = plugin_finder.fetch_plugin(
            [builtin, self._user_plugin]
        )

        self._data_plugins = data_plugins
        self._cache_object = _cache.MemoryCache()
        self._data_locator = tools.DataLocation()

    def parse(self, file_location):
        """
        Parses a single file into memory then passes that data back to the
        main object.

        Args:
            file_location (str): The non-parsed settings from the
                configuration file.

        Returns:
            The data that was loaded in from file.

        Raises:
            definitions.UnknownData: If the loading of the file fails and
                fail on parse error is set to true then this will be
                raised.
        """

        if self._clear_cache:
            cache_location = self._data_locator.find_cache_dir(
                file_location
            )

            try:
                os.remove(cache_location)
            except OSError:
                pass

        if self._cache:
            cache_location = self._data_locator.find_cache_dir(
                file_location
            )

            try:
                return self._cache_object.read_cache(
                    file_location, cache_location
                )

            except _cache.CacheError:
                self._logger.info("No usable cache found.")

        try:
            plugin = self._search(file_location)
        except exceptions.UnknownData:
            if self._fail:
                raise
            else:
                return 0

        returned_parser = plugin.plugin_memory_parser()
        parser = returned_parser()
        data = parser.parse(file_location)

        if self._cache:
            cache_location = self._data_locator.find_cache_dir(
                file_location
            )

            self._cache_object.make_cache(
                data, file_location, cache_location
            )

        return data

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
        if self._cache:
            cache_location = self._data_locator.find_cache_dir(
                file_location
            )

            try:
                self._cache_object.make_cache(
                    data, file_location, cache_location
                )
            except _cache.CacheError:
                pass

        extension = os.path.splitext(file_location)[1]
        length = len(data.shape)
        self._logger.debug("Data's shape is: " + repr(length))
        self._logger.debug("Data's extension is: " + repr(extension))

        for plugin in self._data_plugins:
            the_plugin = plugin()
            supported_length = the_plugin.plugin_supported_length()

            supported_extensions = \
                the_plugin.plugin_supported_extensions()

            if length == supported_length:
                if extension == "" or extension in supported_extensions():
                    returned_parser = the_plugin.plugin_memory_parser()
                    parser = returned_parser()
                    parser.write(file_location, data)
                    return False
        if self._fail:
            raise exceptions.IncompatibleData


class Iterator(templates.DataReaderTemplate, DataCoreTools):
    def __init__(self, fail=True, user_plugin=False, options=False):
        """
        Simple plugin that returns a reader or writer that can read and
        write the requested data.
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

        self._data_plugins = plugin_finder.fetch_plugin(
            [builtin, self._user_plugin]
        )

    def return_reader(self, file_location):
        """
        Searches for the correct reader than passes that back to the
        requesting object.

        Args:
            file_location (str): The line that contains the settings.

        Returns:
            object: The reader that was requested.
            bool: False if it failed to find a reader.

        Raises:
            definitions.UnknownData: If the loading of the file fails and
                fail on parse error is set to true then this will be
                raised.
        """
        try:
            plugin = self._search(file_location)
            return plugin.plugin_reader()
        except exceptions.UnknownData:
            if self._fail:
                raise
            else:
                return 0

    def return_writer(self, file_location):
        """
        Searches for the correct writer than passes that back to the
        requesting object.

        Args:
            file_location (str): The line that contains the settings.

        Returns:
            object: The writer that was requested.
            bool: False if it failed to find a writer

        Raises:
            definitions.UnknownData: If the loading of the file fails and
                fail on parse error is set to true then this will be
                raised.
        """
        try:
            plugin = self._search(file_location)
            return plugin.plugin_writer()
        except exceptions.UnknownData:
            if self._fail:
                raise
            else:
                return 0
