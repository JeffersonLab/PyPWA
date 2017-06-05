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
The Root Storage objects for the configurator.
----------------------------------------------
- _InternalStorage - The true storage of the plugins and shells, should act as
  a singleton.

- Storage - Provides a programmatic interface to the plugins and shells, and
  has the ability to update internal data when called if new plugin locations
  have been added.
"""

import logging
from typing import Any, List

import PyPWA.builtin_plugins
import PyPWA.core
import PyPWA.shell
from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import options
from PyPWA.core.shared import plugin_loader

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _InternalStorage(object):

    plugins = []  # type: List[options.Plugin]
    shells = []  # type: List[options.Main]
    index = 0


class Storage(object):

    __LOGGER = logging.getLogger(__name__ + ".ConfiguratorStorage")
    __STORAGE = _InternalStorage()

    def __init__(self):
        self.__loader = plugin_loader.PluginLoader()
        self.__loader.add_plugin_location(
            {PyPWA.builtin_plugins, PyPWA.shell, PyPWA.core}
        )
        self.__index = 0
        self._check_for_updates()

    def _check_for_updates(self):
        if self.__loader.storage_index < self.__STORAGE.index:
            self.__LOGGER.critical(
                "PluginStorage has a smaller index than Storage! "
                "This means something broke with PluginStorage, and the "
                "program is likely to fail!"
            )
        if not self.__loader.storage_index == self.__STORAGE.index:
            self.__LOGGER.debug(
                "Storage is out of date with plugin module, "
                "refreshing plugins"
            )
            self.__update_storage()

        if not self.__STORAGE.index == self.__index:
            self.__index = self.__STORAGE.index
            self._update_extra()

    def __update_storage(self):
        self.__STORAGE.plugins = self.__loader.get_by_class(options.Plugin)
        self.__STORAGE.shells = self.__loader.get_by_class(options.Main)
        self.__STORAGE.index = self.__loader.storage_index

    def _update_extra(self):
        pass

    def add_location(self, location):
        # type: (Any) -> None
        self.__loader.add_plugin_location(location)
        self._check_for_updates()

    def _get_plugins(self):
        # type: () -> Any
        self._check_for_updates()
        return self.__STORAGE.plugins

    def _get_shells(self):
        # type: () -> Any
        self._check_for_updates()
        return self.__STORAGE.shells
