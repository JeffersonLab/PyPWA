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
Contains PluginSearch and helper private classes. This file is used to load
the data plugins and user plugins then return one of them that can read/write
whatever data needs to be read/written.

- PluginSearch - Searches for data plugins that can read or write the provided
  data.
  
- _FindReadPlugins - searches for a plugin that can read the provided data.

- _FindWritePlugins - Searches for a plugin that can write the given data 
  to the given file extension.
"""

import logging
import os

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import builtin
from PyPWA.builtin_plugins.data import data_templates
from PyPWA.builtin_plugins.data import exceptions
from PyPWA.core.shared import plugin_loader

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class PluginSearch(object):

    __logger = logging.getLogger(__name__ + ".PluginSearch")
    __found_plugins = None

    def __init__(self, user_plugin_dir=""):
        self.__logger.addHandler(logging.NullHandler())
        self.__setup_plugin_storage(user_plugin_dir)
        self.__log_found_plugins()

    def __setup_plugin_storage(self, user_plugin_dir):
        plugin_storage = plugin_loader.PluginLoader()
        plugin_storage.add_plugin_location([builtin, user_plugin_dir])

        found_plugins = plugin_storage.get_by_class(
            data_templates.TemplateDataPlugin
        )

        self.__found_plugins = found_plugins

    def __log_found_plugins(self):
        self.__logger.debug("Loaded Data Plugins: %s" % self.__found_plugins)

    def get_read_plugin(self, file_location):
        plugin_finder = _FindReadPlugins(self.__found_plugins)
        return plugin_finder.get_plugin(file_location)

    def get_write_plugin(self, file_location, data):
        plugin_finder = _FindWritePlugins(self.__found_plugins)
        return plugin_finder.get_plugin(file_location, data)


class _FindReadPlugins(object):

    __logger = logging.getLogger(__name__ + "._FindReadPlugins")
    __potential_plugins = None

    def __init__(self, potential_plugins):
        self.__logger.addHandler(logging.NullHandler())
        self.__potential_plugins = potential_plugins

    def get_plugin(self, file_location):
        return self.__search_plugin_list(file_location)

    def __search_plugin_list(self, file_location):
        for plugin in self.__potential_plugins:
            if self.__plugin_can_read(plugin, file_location):
                return plugin()

        raise exceptions.UnknownData(
            "Unable to find a plugin that can load %s" % file_location
        )

    def __plugin_can_read(self, plugin, file_location):
        try:
            self._run_read_test(plugin, file_location)
            return True
        except exceptions.IncompatibleData:
            self.__logger.debug(
                "Skipping %s for data %s, test failed." %
                (plugin.__name__, file_location)
            )
            return False
        except Exception as Error:
            # We don't want a plugin to halt execution, but we do want to know
            # that a plugin failed to load and why.
            self.__logger.exception(Error)
            return False

    def _run_read_test(self, plugin, file_location):
        read_test = plugin().get_plugin_read_test()
        read_test.quick_test(file_location)
        self.__logger.info(
            "Found '%s' will load '%s'" % (plugin.__name__, file_location)
        )


class _FindWritePlugins(object):

    __data_is_gamp = False
    __data_is_flat = False
    __file_extension = ""
    __file_name = ""
    __logger = logging.getLogger(__name__ + "._FindWritePlugins")
    __potential_plugins = None

    def __init__(self, potential_plugins):
        self.__logger.addHandler(logging.NullHandler())
        self.__potential_plugins = potential_plugins

    def get_plugin(self, file_location, data):
        self.__set_data_type(data)
        self.__set_data_extension(file_location)
        return self.__search_for_plugins()

    def __set_data_type(self, data):
        shape_count = len(data.shape)

        if shape_count == 3:
            self.__logger.debug("Found data type: GAMP")
            self.__data_is_gamp = True
        elif shape_count == 1:
            self.__logger.debug("Found data type: Flat")
            self.__data_is_flat = True
        else:
            self.__logger.error(
                "Found noise, data shape_count is: " + str(shape_count)
            )

            raise exceptions.UnknownData

    def __set_data_extension(self, file_location):
        split_extension = os.path.splitext(file_location)
        extension = split_extension[1]
        self.__file_extension = extension
        self.__file_name = file_location

        self.__logger.debug("Data's extension is: " + repr(extension))

    def __search_for_plugins(self):
        for plugin in self.__potential_plugins:
            the_plugin = plugin()
            if self.__check_plugin(the_plugin):
                self.__log_found_plugin(the_plugin)
                return the_plugin

        raise exceptions.UnknownData

    def __check_plugin(self, the_plugin):
        supported_extensions = the_plugin.plugin_supported_extensions
        if self.__supports_data_type(the_plugin):
            if self.__supports_file_extension(supported_extensions):
                return True

        return False

    def __supports_data_type(self, plugin):
        if self.__data_is_flat:
            return plugin.plugin_supports_flat_data
        elif self.__data_is_gamp:
            return plugin.plugin_supports_gamp_data

    def __supports_file_extension(self, extensions):
        if self.__file_extension == "":
            self.__logger.warning(
                "No extension found! Will use first data match! This could "
                "result in strange or unusual data in your file! Considering "
                "using an extension in the future!"
            )
            return True
        elif self.__file_extension in extensions:
            self.__logger.debug(
                "Found %s in %s!" % (self.__file_extension, repr(extensions))
            )
            return True
        else:
            self.__logger.info("Extension not supported!")
            return False

    def __log_found_plugin(self, plugin):
        self.__logger.info(
            "Found '%s' to write '%s'" % (
                plugin.plugin_name, self.__file_name
            )
        )
