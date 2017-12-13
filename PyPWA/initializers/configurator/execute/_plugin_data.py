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
Plugin Setup
------------
This source file is file that initializes the plugins for use in the main 
program.

- _RequestedPlugins - Takes the ids from the settings and uses it to grab the
  metadata for all the plugins listed in the configuration file, plugins
  are loaded into loaded_plugin_metadata and the main is loaded 
  into loaded_main_metadata.

- SetupProgram - Takes the settings object and uses that to initialize all of
  the plugins. Exposes execute to begin the main program.
"""

import logging
from typing import List

from PyPWA import AUTHOR, VERSION
from PyPWA.initializers.configurator import options as opts
from PyPWA.initializers.configurator.execute import _settings, _storage_data

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _RequestedPlugins(object):

    __LOGGER = logging.getLogger(__name__ + "._RequestedPlugins")

    def __init__(self, program_name):
        # type: (str) -> None
        self.__storage = _storage_data.ModulePicking()
        self.__program_name = program_name
        self.__program = None  # type: opts.Program
        self.__find_metadata()

    def __find_metadata(self):
        potential_main = self.__get_potential()
        self.__process_potential(potential_main)

    def __get_potential(self):
        # type: (str) -> opts.Program
        return self.__storage.request_program_by_id(self.__program_name)

    def __process_potential(self, potential_main):
        # type: (opts.Program, str) -> None
        if potential_main:
            self.__LOGGER.debug(
                "Found the program: '%s'!" % potential_main.name
            )
            self.__program = potential_main
        else:
            raise ValueError("Failed to find '%s'!" % self.__program_name)

    @property
    def loaded_program_metadata(self):
        # type: () -> opts.Program
        return self.__program


class SetupProgram(object):

    def __init__(self, settings_setup):
        # type: (_settings.Setup) -> None
        self.__settings_setup = settings_setup  # type: _settings.Setup
        self.__program = None  # type: _RequestedPlugins

    def setup(self):
        requested = _RequestedPlugins(self.__settings_setup.program_name)
        self.__program = requested.loaded_program_metadata

    def execute(self):
        program = self.__program.get_start()
        program.start()
