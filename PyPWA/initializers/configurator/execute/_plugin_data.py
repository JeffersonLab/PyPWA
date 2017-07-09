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

- _InitializePlugin - Takes the settings and metadata for a plugin and uses
  it to load and extract the actual executed plugin.
  
- _SetupPlugins - Contains the main loop needed to initialize all the plugins,
  loads the plugins into a dictionary where the key is the plugin type, and
  exposes that dictionary through loaded_plugins.
  
- _SetupMain - Takes all of the objects and uses them to load the plugin data
  into the settings for the main, then initializes the main and exposes that
  through main_program.
  
- SetupProgram - Takes the settings object and uses that to initialize all of
  the plugins. Exposes execute to begin the main program.
"""

import logging
from typing import Any, Dict, List
from typing import Optional as Opt

from PyPWA import AUTHOR, VERSION
from PyPWA.initializers.configurator import option_tools
from PyPWA.initializers.configurator import options as opts
from PyPWA.initializers.configurator.execute import _settings
from PyPWA.initializers.configurator.execute import _storage_data
from PyPWA.libs.interfaces import common

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _RequestedPlugins(object):

    __LOGGER = logging.getLogger(__name__ + "._RequestedPlugins")

    def __init__(self, the_ids):
        # type: (List[str]) -> None
        self.__storage = _storage_data.ModulePicking()
        self.__the_ids = the_ids
        self.__plugins = []
        self.__main = None  # type: opts.Main
        self.__find_metadata()

    def __find_metadata(self):
        for the_id in self.__the_ids:
            self.__LOGGER.debug("Scanning plugins for '%s'" % the_id)
            self.__check_metadata(the_id)

    def __check_metadata(self, the_id):
        # type: (str) -> None
        potential_main, potential_plugin = self.__get_potential(the_id)
        self.__process_potential(potential_main, potential_plugin, the_id)

    def __get_potential(self, the_id):
        # type: (str) -> List[Opt[opts.Main], Opt[opts.Plugin]]
        potential_main = self.__storage.request_main_by_id(the_id)
        potential_plugin = self.__storage.request_plugin_by_name(the_id)

        return [potential_main, potential_plugin]

    def __process_potential(self, potential_main, potential_plugin, the_id):
        # type: (Opt[opts.Main], Opt[opts.Plugin], str) -> None
        if potential_main:
            self.__LOGGER.debug(
                "Found that '%s' is the main" % potential_main.plugin_name
            )
            self.__main = potential_main
        elif potential_plugin:
            self.__LOGGER.debug(
                "Found that '%s' is a plugin" % potential_plugin.plugin_name
            )
            self.__plugins.append(potential_plugin)
        else:
            raise ValueError("Unknown plugin %s" % the_id)

    @property
    def loaded_plugin_metadata(self):
        # type: () -> List[opts.Plugin]
        return self.__plugins

    @property
    def loaded_main_metadata(self):
        # type: () -> opts.Main
        return self.__main


class _InitializePlugin(object):

    __LOGGER = logging.getLogger(__name__ + "._InitializePlugin")

    @classmethod
    def initialize(cls, metadata, settings):
        # type: (opts.Base, Dict[str, Any]) -> Any
        cls.__LOGGER.debug("Initializing '%s'" % metadata.plugin_name)
        command = cls.__get_command_object(metadata, settings)
        return cls.__get_interface(metadata, command)

    @staticmethod
    def __get_command_object(metadata, settings):
        # type: (opts.Base, Dict[str, Any]) -> option_tools.CommandOptions
        default = metadata.default_options
        loaded_settings = settings[metadata.plugin_name]
        return option_tools.CommandOptions(default, loaded_settings)

    @staticmethod
    def __get_interface(metadata, command):
        # type: (opts.Base, option_tools.CommandOptions) -> Any
        setup = metadata.setup(command)
        return setup.return_interface()


class _SetupPlugins(object):

    __LOGGER = logging.getLogger(__name__ + "_SetupPlugins")

    def __init__(self, settings, loaded_modules):
        # type: (Dict[str, Any], _RequestedPlugins) -> None
        self.__settings = settings
        self.__selected_modules = loaded_modules
        self.__plugins = {}
        self.__setup_plugins()

    def __setup_plugins(self):
        self.__LOGGER.info("Initializing plugins.")
        for metadata in self.__selected_modules.loaded_plugin_metadata:
            self.__LOGGER.debug("Plugin Type: '%s'" % repr(metadata))
            self.__process_plugin(metadata)

    def __process_plugin(self, metadata):
        # type: (opts.Plugin) -> None
        plugin = _InitializePlugin.initialize(metadata, self.__settings)
        self.__plugins[metadata.provides.name] = plugin

    @property
    def loaded_plugins(self):
        # type: () -> Dict[str, opts.Plugin]
        return self.__plugins


class _SetupMain(object):

    __LOGGER = logging.getLogger(__name__ + "_SetupMain")

    def __init__(self, settings, loaded_modules, loaded_plugins):
        # type: (Dict[str, Any], _RequestedPlugins, _SetupPlugins) -> None
        self.__settings = settings
        self.__selected_modules = loaded_modules
        self.__plugins = loaded_plugins
        self.__name = loaded_modules.loaded_main_metadata.plugin_name
        self.__main = None  # type: common.Main
        self.__setup_main()

    def __setup_main(self):
        self.__add_plugins_to_settings()
        self.__main = _InitializePlugin.initialize(
            self.__selected_modules.loaded_main_metadata, self.__settings
        )

    def __add_plugins_to_settings(self):
        for key, value in self.__plugins.loaded_plugins.items():
            self.__LOGGER.debug("Adding '%s' to main's settings" % key)
            self.__settings[self.__name][key] = value

    @property
    def main_program(self):
        # type: () -> common.Main
        return self.__main


class SetupProgram(object):

    def __init__(self, settings_setup):
        # type: (_settings.Setup) -> None
        self.__settings_setup = settings_setup  # type: _settings.Setup
        self.__selected_plugins = None  # type: _RequestedPlugins
        self.__plugins = None  # type: _SetupPlugins
        self.__main = None  # type: _SetupMain

    def setup(self):
        self.__determine_plugins()
        self.__load_plugins()
        self.__load_main()

    def __determine_plugins(self):
        self.__selected_plugins = _RequestedPlugins(
            self.__settings_setup.plugin_ids
        )

    def __load_plugins(self):
        self.__plugins = _SetupPlugins(
            self.__settings_setup.loaded_settings, self.__selected_plugins
        )

    def __load_main(self):
        self.__main = _SetupMain(
            self.__settings_setup.loaded_settings,
            self.__selected_plugins, self.__plugins
        )

    def execute(self):
        program = self.__main.main_program
        program.start()
