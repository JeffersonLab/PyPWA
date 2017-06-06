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
Execute Tools, general libs needed to build the program.
--------------------------------------------------------
- ModulePicking - This loads all the plugins, then parses their templates 
  into one massive template dictionary.

- Templates - Allows the program to fetch plugins and mains by their 
  name so that the names inside the configuration file can match up to their 
  respected plugin.
"""

import logging

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import storage
from PyPWA.core.configurator import options

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ModulePicking(storage.Storage):

    def __init__(self):
        super(ModulePicking, self).__init__()

    def request_main_by_id(self, the_id):
        # type: (str) -> options.Main
        for main in self._get_shells():
            if main.plugin_name == the_id:
                return main

    def request_plugin_by_name(self, name):
        # type: (str) -> options.Plugin
        for plugin in self._get_plugins():
            if plugin.plugin_name == name:
                return plugin


class Templates(storage.Storage):

    __LOGGER = logging.getLogger(__name__ + ".Templates")

    def __init__(self):
        super(Templates, self).__init__()
        self.__templates = None  # type: dict
        self._update_extra()

    def _update_extra(self):
        self.__templates = {}
        self.__process_options()
        self.__process_main()

    def __process_options(self):
        for plugin in self._get_plugins():
            self.__add_module(plugin)

    def __process_main(self):
        for main in self._get_shells():
            self.__add_module(main)

    def __add_module(self, main):
        # type: (options.Main) -> None
        self.__templates[main.plugin_name] = main.option_types

    def get_templates(self):
        self._check_for_updates()
        return self.__templates
