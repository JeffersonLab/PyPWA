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
Contains PluginSearch and helper private classes. This file is used to load
the data plugins and user plugins then return one of them that can read/write
whatever data needs to be read/written.
"""

import logging
import os

from PyPWA.builtin_plugins.data import builtin
from PyPWA.builtin_plugins.data import data_templates
from PyPWA.builtin_plugins.data import exceptions
from PyPWA.core import plugin_loader


class PluginSearch(object):

    _logger = logging.getLogger(__name__)
    _found_plugins = plugin_loader.PluginLoading

    def __init__(self, user_plugin_dir=""):
        self._logger.addHandler(logging.NullHandler())
        self._setup_plugin_storage(user_plugin_dir)

    def _setup_plugin_storage(self, user_plugin_dir):
        plugin_storage = plugin_loader.PluginLoading(
            data_templates.TemplateDataPlugin
        )

        found_plugins = plugin_storage.fetch_plugin(
            [builtin, user_plugin_dir]
        )

        self._found_plugins = found_plugins

    def get_read_plugin(self, file_location):
        plugin_finder = _FindReadPlugins(self._found_plugins)
        return plugin_finder.get_plugin(file_location)

    def get_write_plugin(self, file_location, data):
        plugin_finder = _FindWritePlugins(self._found_plugins)
        return plugin_finder.get_plugin(file_location, data)


class _FindReadPlugins(object):

    _logger = logging.getLogger(__name__)
    _potential_plugins = plugin_loader.PluginLoading

    def __init__(self, potential_plugins):
        self._logger.addHandler(logging.NullHandler())
        self._potential_plugins = potential_plugins

    def get_plugin(self, file_location):
        return self._search_plugin_list(file_location)

    def _search_plugin_list(self, file_location):
        for plugin in self._potential_plugins:
            if self._plugin_can_read(plugin, file_location):
                return plugin()

        raise exceptions.UnknownData(
            "Unable to find a plugin that can load %s" % file_location
        )

    def _plugin_can_read(self, plugin, file_location):
        try:
            self._run_read_test(plugin, file_location)
            return True
        except exceptions.IncompatibleData:
            self._logger.debug(
                "Skipping %s for data %s, test failed." %
                (plugin.__name__, file_location)
            )
            return False
        except Exception as Error:
            # We don't want a plugin to halt execution, but we do want to know
            # that a plugin failed to load and why.
            self._logger.exception(Error)
            return False

    def _run_read_test(self, plugin, file_location):
        read_test = plugin().get_plugin_read_test()
        read_test.quick_test(file_location)
        self._logger.info(
            "Found %s will load %s" % (plugin.__name__, file_location)
        )


class _FindWritePlugins(object):

    _data_is_gamp = False
    _data_is_flat = False
    _file_extension = ""
    _logger = logging.getLogger(__name__)
    _potential_plugins = plugin_loader.PluginLoading

    def __init__(self, potential_plugins):
        self._logger.addHandler(logging.NullHandler())
        self._potential_plugins = potential_plugins

    def get_plugin(self, file_location, data):
        self._set_data_type(data)
        self._set_data_extension(file_location)
        return self._search_for_plugins()

    def _set_data_type(self, data):
        shape_count = len(data.shape)

        if shape_count == 3:
            self._logger.info("Found data type: GAMP")
            self._data_is_gamp = True
        elif shape_count == 1:
            self._logger.info("Found data type: Flat")
            self._data_is_flat = True
        else:
            self._logger.info(
                "Found noise, data shape_count is: " + str(shape_count)
            )

            raise exceptions.UnknownData

    def _set_data_extension(self, file_location):
        split_extension = os.path.splitext(file_location)
        extension = split_extension[1]
        self._file_extension = extension

        self._logger.debug("Data's extension is: " + repr(extension))

    def _search_for_plugins(self):
        for plugin in self._potential_plugins:
            the_plugin = plugin()
            if self._check_plugin(the_plugin):
                return the_plugin

        raise exceptions.UnknownData

    def _check_plugin(self, the_plugin):
        supported_extensions = the_plugin.plugin_supported_extensions
        if self._supports_data_type(the_plugin):
            if self._supports_file_extension(supported_extensions):
                return True

        return False

    def _supports_data_type(self, plugin):
        if self._data_is_flat:
            return plugin.plugin_supports_flat_data
        elif self._data_is_gamp:
            return plugin.plugin_supports_gamp_data

    def _supports_file_extension(self, extensions):
        if self._file_extension == "":
            self._logger.warn(
                "No extension found! Will use first data match! This could "
                "result in strange or unusual data in your file! Considering "
                "using an extension in the future!"
            )
            return True
        elif self._file_extension in extensions:
            self._logger.info(
                "Found %s in %s!" % (self._file_extension, repr(extensions))
            )
            return True
        else:
            self._logger.info("Extension not supported!")
            return False
