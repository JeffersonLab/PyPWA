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
from PyPWA.initializers.configurator import options, storage

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ModulePicking(storage.Storage):

    def __init__(self):
        super(ModulePicking, self).__init__()

    def request_program_by_id(self, the_id):
        # type: (str) -> options.Program
        for main in self._get_programs():
            if main.name == the_id:
                return main

    def request_component_by_name(self, name):
        # type: (str) -> options.Component
        for plugin in self._get_components():
            if plugin.name == name:
                return plugin


class Templates(storage.Storage):

    __LOGGER = logging.getLogger(__name__ + ".Templates")

    def __init__(self):
        super(Templates, self).__init__()
        self.__templates = None  # type: dict
        self._update_extra()

    def _update_extra(self):
        self.__templates = {}
        self.__process_components()
        self.__process_programs()

    def __process_components(self):
        for component in self._get_components():
            self.__add_module(component)

    def __process_programs(self):
        for program in self._get_programs():
            self.__add_module(program)

    def __add_module(self, main):
        # type: (options.Component) -> None
        try:
            self.__templates[main.name] = main.get_option_types()
        except NotImplementedError:
            raise RuntimeError(
                "%s does not implement the necessary methods!" % repr(main)
            )

    def get_templates(self):
        self._check_for_updates()
        return self.__templates
