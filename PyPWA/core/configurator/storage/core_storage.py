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

import PyPWA.builtin_plugins
import PyPWA.core
import PyPWA.shell
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core.configurator import options
from PyPWA.core.shared import plugin_loader

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ModuleStorage(object):

    __plugin_locations = {PyPWA.builtin_plugins, PyPWA.shell, PyPWA.core}
    __plugin_storage = None  # type: plugin_loader.PluginStorage()
    __plugins = None  # type: list
    __shell = None  # type: list

    def __init__(self, extra_locations=False):
        if extra_locations:
            self.__process_extra_locations(extra_locations)
        self.__set_plugin_storage()
        self.__set_plugins()
        self.__set_shell()

    def __process_extra_locations(self, locations):
        if isinstance(locations, str):
            self.__plugin_locations.add(locations)
        elif isinstance(locations, type(PyPWA)):
            self.__plugin_locations.add(locations)
        elif isinstance(locations, list):
            for location in locations:
                self.__process_extra_locations(location)

    def __set_plugin_storage(self):
        self.__plugin_storage = plugin_loader.PluginStorage()
        self.__plugin_storage.add_plugin_location(self.__plugin_locations)

    def __set_plugins(self):
        self.__plugins = self.__plugin_storage.get_by_class(options.Plugin)

    def __set_shell(self):
        self.__shell = self.__plugin_storage.get_by_class(options.Main)

    @property
    def shell_modules(self):
        return self.__shell

    @property
    def option_modules(self):
        return self.__plugins


class MetadataStorage(object):

    __logger = logging.getLogger(__name__)
    __actual_storage = None  # type: {}

    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())
        self.__actual_storage = {}

    def add_plugins(self, plugins):
        for plugin in plugins:
            loaded_plugin = self.__get_initialized_plugin(plugin)

            if not isinstance(loaded_plugin, type(None)):
                self.__add_type(loaded_plugin)
                self.__plugin_filter(plugin, loaded_plugin)

    def __get_initialized_plugin(self, plugin):
        try:
            temp_object = plugin()
            return temp_object
        except Exception as Error:
            self.__logger.error(Error)

    def __add_type(self, plugin):
        plugin_type = self.__get_plugin_type(plugin)
        if not self.__plugin_type_included(plugin_type):
            self.__actual_storage[plugin_type] = []

    @staticmethod
    def __get_plugin_type(plugin):
        return plugin.provides

    def __plugin_type_included(self, plugin_type):
        if plugin_type in self.__actual_storage.keys():
            return True
        else:
            return False

    def __plugin_filter(self, plugin, loaded_plugin):
        plugin_type = self.__get_plugin_type(loaded_plugin)
        self.__actual_storage[plugin_type].append(plugin)

    def search_plugin(self, plugin_name, plugin_type):
        if self.__plugin_type_included(plugin_type):
            return self.__plugin_name_search(plugin_name, plugin_type)
        else:
            self.__cant_find_plugin(plugin_name)

    def __plugin_name_search(self, plugin_name, plugin_type):
        for plugin in self.__actual_storage[plugin_type]:
            name = self.__get_plugin_name(plugin)
            if name == plugin_name:
                return plugin
        self.__cant_find_plugin(plugin_name)

    def __get_plugin_name(self, plugin):
        loaded_plugin = self.__get_initialized_plugin(plugin)
        return loaded_plugin.plugin_name

    def __cant_find_plugin(self, plugin_name):
        error = "Failed to find plugin {0}".format(plugin_name)
        self.__logger.error(error)
        raise ImportError(error)

    def request_plugin_by_type(self, plugin_type):
        if self.__plugin_type_included(plugin_type):
            return self.__actual_storage[plugin_type]
