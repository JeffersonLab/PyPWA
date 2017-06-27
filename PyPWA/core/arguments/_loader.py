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
Loader for Argument Parser
--------------------------
Loads the plugins for the Argument Parser with a simple parser around
the core lib plugin loader.

- _plugin_charger - Loads the plugin search locations

- _PluginStorage - Loads all the potential plugins into a list and makes it
  accessible publicly

- RequestedFetcher - The main entry for the ArgumentParser Plugin Loading,
  allows for plugins to be searched for by their name exclusively.
"""

from typing import List
from typing import Optional as Opt

import PyPWA.builtin_plugins
import PyPWA.shell
from PyPWA import AUTHOR, VERSION
from PyPWA.core.arguments import arguments_options
from PyPWA.core.shared import plugin_loader

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


def _plugin_charger(optional_plugin_location):
    # type: (Opt[str]) -> None
    loader = plugin_loader.PluginLoader()
    loader.add_plugin_location(optional_plugin_location)
    loader.add_plugin_location({PyPWA.shell, PyPWA.builtin_plugins})


class _PluginStorage(object):

    def __init__(self):
        self.__loader = plugin_loader.PluginLoader()
        self.__storage = []
        self.__load_main_plugins()
        self.__load_option_plugins()

    def __load_main_plugins(self):
        for main in self.__loader.get_by_class(arguments_options.Main):
            self.__storage.append(main)

    def __load_option_plugins(self):
        for option in self.__loader.get_by_class(arguments_options.Plugin):
            self.__storage.append(option)

    @property
    def storage(self):
        # type: () -> List[arguments_options.Base]
        return self.__storage


class RequestedFetcher(object):

    def __init__(self, optional_plugin_location=None):
        # type: (Opt[str]) -> None
        _plugin_charger(optional_plugin_location)
        self.__storage = _PluginStorage()

    def get_plugin_by_name(self, name):
        # type: (str) -> arguments_options.Base
        for plugin in self.__storage.storage:
            if plugin.get_name() == name:
                return plugin
        raise ValueError("%s not found!" % name)
