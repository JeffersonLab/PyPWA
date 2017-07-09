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
Handles direct interaction with plugins
---------------------------------------

- MetadataStorage - Interacts directly with the plugins.
- GetPluginList - Stores the dependency plugins for the configuration.
"""

import logging

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import options
from PyPWA.core.configurator import storage
from PyPWA.core.configurator.create_config import _questions
from typing import Any, Dict, Union, List

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION

__STORAGE_TYPE = Dict[Union[str, options.Types], Any]


class MetadataStorage(storage.Storage):

    __LOGGER = logging.getLogger(__name__)

    def __init__(self):
        super(MetadataStorage, self).__init__()
        self.__actual_storage = None  # type: __STORAGE_TYPE
        self._update_extra()

    def _update_extra(self):
        self.__actual_storage = {}
        for plugin in self._get_plugins():
            self.__add_type(plugin)
            self.__append_plugin(plugin)

    def __add_type(self, plugin):
        # type: (options.Plugin) -> None
        if plugin.provides not in self.__actual_storage:
            self.__actual_storage[plugin.provides] = []

    def __append_plugin(self, plugin):
        # type: (options.Plugin) -> None
        self.__actual_storage[plugin.provides].append(plugin)

    def search_plugin(self, plugin_name, plugin_type):
        # type: (str, options.Types) -> options.Plugin
        if plugin_type in self.__actual_storage:
            return self.__plugin_name_search(plugin_name, plugin_type)
        else:
            self.__cant_find_plugin(plugin_name)

    def __plugin_name_search(self, plugin_name, plugin_type):
        # type: (str, options.Types) -> options.Plugin
        for plugin in self.__actual_storage[plugin_type]:
            if plugin.plugin_name == plugin_name:
                return plugin
        self.__cant_find_plugin(plugin_name)

    @staticmethod
    def __cant_find_plugin(plugin_name):
        # type: (str) -> None
        error = "Failed to find plugin {0}".format(plugin_name)
        raise ValueError(error)

    def request_plugins_by_type(self, plugin_type):
        # type: (options.Types) -> List[options.Plugin]
        if plugin_type in self.__actual_storage:
            return self.__actual_storage[plugin_type]
        else:
            raise ValueError("Unknown plugin type: %s!" % plugin_type)

    def request_main_plugin_by_name(self, name):
        # type: (str) -> options.Plugin
        for plugin in self._get_shells():
            if plugin.plugin_name == name:
                return plugin
        raise ValueError("Unknown program name '%s'" % name)


class GetPluginList(object):

    __LOGGER = logging.getLogger(__name__)

    def __init__(self):
        self.__ask_for_plugin = _questions.GetSpecificPlugin()
        self.__storage = MetadataStorage()
        self.__plugin_list = []  # type: List[options.Plugin]
        self.__main_plugin = None  # type: options.Main

    def parse_plugins(self, main_plugin):
        # type: (options.Main) -> None
        for plugin_type in options.Types:
            if plugin_type in main_plugin.required_plugins:
                self.__plugin_list.append(self.__process_plugins(plugin_type))
        self.__main_plugin = main_plugin

    def __process_plugins(self, plugin_type):
        # type: (options.Types) -> options.Plugin
        plugin_list = self.__storage.request_plugins_by_type(plugin_type)
        if len(plugin_list) == 1:
            return plugin_list[0]
        else:
            self.__ask_for_plugin.ask_for_plugin(plugin_list, plugin_type)
            name = self.__ask_for_plugin.get_specific_plugin()

            the_chosen_one = self.__storage.search_plugin(name, plugin_type)
            return the_chosen_one

    @property
    def plugins(self):
        # type: () -> List[options.Plugin]
        return self.__plugin_list

    @property
    def program(self):  # needed so that BuildConfig can know the program plugin
        # type: () -> options.Main
        return self.__main_plugin
