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
Takes all the loaded plugins and searches through them for plugins matching 
a name or plugins matching a type.
"""

import logging

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import storage

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class MetadataStorage(storage.Storage):

    __logger = logging.getLogger(__name__)
    __actual_storage = None  # type: {}

    def __init__(self):
        super(MetadataStorage, self).__init__()
        self.__logger.addHandler(logging.NullHandler())
        self._update_extra()

    def _update_extra(self):
        self.__actual_storage = {}
        for plugin in self._get_plugins():
            self.__add_type(plugin)
            self.__append_plugin(plugin)

    def __add_type(self, plugin):
        if plugin.provides not in self.__actual_storage:
            self.__actual_storage[plugin.provides] = []

    def __append_plugin(self, plugin):
        self.__actual_storage[plugin.provides].append(plugin)

    def search_plugin(self, plugin_name, plugin_type):
        if plugin_type in self.__actual_storage:
            return self.__plugin_name_search(plugin_name, plugin_type)
        else:
            self.__cant_find_plugin(plugin_name)

    def __plugin_name_search(self, plugin_name, plugin_type):
        for plugin in self.__actual_storage[plugin_type]:
            if plugin.plugin_name == plugin_name:
                return plugin
        self.__cant_find_plugin(plugin_name)

    @staticmethod
    def __cant_find_plugin(plugin_name):
        error = "Failed to find plugin {0}".format(plugin_name)
        raise ValueError(error)

    def request_plugins_by_type(self, plugin_type):
        if plugin_type in self.__actual_storage:
            return self.__actual_storage[plugin_type]
        else:
            raise ValueError("Unknown plugin type: %s!" % plugin_type)
