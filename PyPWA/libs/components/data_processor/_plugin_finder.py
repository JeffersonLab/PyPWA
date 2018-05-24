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
import numpy
from typing import List, Union

from PyPWA.libs.math import particle
from PyPWA import Path, AUTHOR, VERSION, builtin_plugins
from PyPWA.libs import plugin_loader
from PyPWA.libs.components.data_processor import (
    data_templates, exceptions, SUPPORTED_DATA_TYPE
)

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class PluginSearch(object):

    __LOGGER = logging.getLogger(__name__ + ".PluginSearch")

    def __init__(self, user_plugin_dir=""):
        # type: (Union[str, Path]) -> None
        self.__found_plugins = None
        self.__setup_plugin_storage(Path(user_plugin_dir))
        self.__log_found_plugins()

    def __setup_plugin_storage(self, user_plugin_dir):
        # type: (Path) -> None
        plugin_storage = plugin_loader.PluginLoader()
        plugin_storage.add_plugin_location([builtin_plugins, user_plugin_dir])

        found_plugins = plugin_storage.get_by_class(
            data_templates.DataPlugin
        )

        self.__found_plugins = found_plugins

    def __log_found_plugins(self):
        self.__LOGGER.debug("Loaded Data Plugins: %s" % self.__found_plugins)

    def get_read_plugin(self, file_location):
        # type: (Path) -> data_templates.DataPlugin
        plugin_finder = _FindReadPlugins(self.__found_plugins)
        return plugin_finder.get_plugin(file_location)

    def get_write_plugin(self, file_location, data):
        # type: (Path, SUPPORTED_DATA_TYPE) -> data_templates.DataPlugin
        plugin_finder = _FindWritePlugins(self.__found_plugins)
        return plugin_finder.get_plugin(file_location, data)


class _FindReadPlugins(object):

    __LOGGER = logging.getLogger(__name__ + "._FindReadPlugins")

    def __init__(self, potential_plugins):
        # type: (List[data_templates.DataPlugin]) -> None
        self.__potential_plugins = potential_plugins

    def get_plugin(self, file_location):
        # type: (Path) -> data_templates.DataPlugin
        return self.__search_plugin_list(file_location)

    def __search_plugin_list(self, file_location):
        # type: (Path) -> data_templates.DataPlugin
        for plugin in self.__potential_plugins:
            if self.__plugin_can_read(plugin, file_location):
                return plugin

        raise exceptions.UnknownData(
            "Unable to find a plugin that can load %s" % file_location
        )

    def __plugin_can_read(self, plugin, file_location):
        # type: (data_templates.DataPlugin, Path) -> bool
        try:
            self.__run_read_test(plugin, file_location)
            return True
        except exceptions.IncompatibleData:
            self.__LOGGER.debug(
                "Skipping %s for data %s, test failed." %
                (plugin.plugin_name, file_location)
            )
            return False
        except Exception as Error:
            # We don't want a plugin to halt execution, but we do want to know
            # that a plugin failed to load and why.
            self.__LOGGER.debug(repr(Error))
            return False

    def __run_read_test(self, plugin, file_location):
        # type: (data_templates.DataPlugin, Path) -> None
        read_test = plugin.get_plugin_read_test()
        read_test.test(file_location)
        self.__LOGGER.info(
            "Found '%s' will load '%s'" % (plugin.plugin_name, file_location)
        )


class _FindWritePlugins(object):

    __LOGGER = logging.getLogger(__name__ + "._FindWritePlugins")

    def __init__(self, potential_plugins):
        # type: (List[data_templates.DataPlugin]) -> None
        self.__potential_plugins = potential_plugins
        self.__data_is_pool = False
        self.__data_is_columned = False
        self.__data_is_single_array = False
        self.__file_extension = ""
        self.__file_name = None  # type: Path

    def get_plugin(self, file_location, data):
        # type: (Path, SUPPORTED_DATA_TYPE) -> data_templates.DataPlugin
        self.__set_data_type(data)
        self.__set_data_extension(file_location)
        return self.__search_for_plugins()

    def __set_data_type(self, data):
        # type: (SUPPORTED_DATA_TYPE) -> None
        if isinstance(data, particle.ParticlePool):
            self.__LOGGER.debug("Found data type: ParticlePool")
            self.__data_is_pool = True
        elif isinstance(data, numpy.ndarray):
            if len(data.shape) != 1:
                self.__LOGGER.error(
                    "Found noise, data shape is: " + str(data.shape)
                )
                raise exceptions.UnknownData("Array Type is Unknown!")
            elif data.dtype.names:
                self.__LOGGER.debug("Found data type: Structured Array")
                self.__data_is_columned = True
            else:
                self.__LOGGER.debug("Found data type: Array")
                self.__data_is_single_array = True
        else:
            raise exceptions.UnknownData(
                "Unknown data type: %s!" % type(data)
            )

    def __set_data_extension(self, file_location):
        # type: (Path) -> None
        self.__file_extension = file_location.suffix
        self.__file_name = file_location
        self.__LOGGER.debug("Data's extension is: %s" % file_location.suffix)

    def __search_for_plugins(self):
        # type: () -> data_templates.DataPlugin
        for plugin in self.__potential_plugins:
            if self.__check_plugin(plugin):
                self.__log_found_plugin(plugin)
                return plugin

        raise exceptions.UnknownData(
            "No plugin reports supporting %s! Check your extension." %
            self.__file_name
        )

    def __check_plugin(self, the_plugin):
        # type: (data_templates.DataPlugin) -> bool
        supported_extensions = the_plugin.plugin_supported_extensions
        if self.__supports_data_type(the_plugin):
            if self.__supports_file_extension(supported_extensions):
                return True

        return False

    def __supports_data_type(self, plugin):
        # type: (data_templates.DataPlugin) -> bool
        if self.__data_is_columned:
            return plugin.plugin_supports_columned_data
        elif self.__data_is_single_array:
            return plugin.plugin_supports_single_array
        elif self.__data_is_pool:
            return plugin.plugin_supports_particle_pool

    def __supports_file_extension(self, extensions):
        # type: (List[str]) -> bool
        if self.__file_extension == "":
            self.__LOGGER.warning(
                "No extension found! Will use first data match! This could "
                "result in strange or unusual data in your file! Considering "
                "using an extension in the future!"
            )
            return True
        elif self.__file_extension in extensions:
            self.__LOGGER.debug(
                "Found %s in %s!" % (self.__file_extension, repr(extensions))
            )
            return True
        else:
            self.__LOGGER.info("Extension not supported!")
            return False

    def __log_found_plugin(self, plugin):
        # type: (data_templates.DataPlugin) -> None
        self.__LOGGER.info(
            "Found '%s' to write '%s'" % (
                plugin.plugin_name, self.__file_name
            )
        )
