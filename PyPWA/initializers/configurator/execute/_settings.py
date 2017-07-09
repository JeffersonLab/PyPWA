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
The main file for handing configuration parsing.
------------------------------------------------
This file contains a collection of objects that load and process the 
configuration file into a usable dictionary that can be used to setup the 
plugins. This configuration file also goes through a sort of spell check to 
ensure that all the keys and values are of the right type for the plugin that
is going to be rendering it.

.. seealso::
    _correct_configuration.py for the logic regarding setting value 
    correction.

- _InternalizeSettings - Takes the settings loaded from the configuration, 
  and replaces select keys in the configuration with keys from the settings 
  override in the entry function. Useful so that you can have multiple names
  for the same main module.
  
- _SetupPluginDir - Static Object that pulls the plugin directory from the 
  configuration and adds the path to the storage objects plugin search path.
  
- Setup - Takes the configuration and override information then parses that 
  information into a usable configuration dictionary.
"""

import logging
from typing import Any, Dict, List

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import storage
from PyPWA.core.configurator.execute import _correct_configuration
from PyPWA.core.configurator.execute import _reader

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _InternalizeSettings(object):

    __LOGGER = logging.getLogger(__name__ + "._InternalizeSettings")

    def __init__(self):
        self.__settings = None
        self.__overrides = None

    def processed_settings(self, settings, settings_overrides):
        # type: (Dict[str, Any], Dict[str, Any]) -> Dict[str, Any]
        self.__settings = settings
        self.__overrides = settings_overrides
        self.__process()
        return self.__settings

    def __process(self):
        self.__override_settings()
        self.__convert_name()

    def __override_settings(self):
        if "main options" in self.__overrides:
            self.__process_overrides()
        else:
            self.__LOGGER.debug("Failed to find main options")

    def __process_overrides(self):
        for key in self.__overrides["main options"]:
            self.__settings[self.__overrides["main name"]][key] = \
                self.__overrides["main options"][key]

    def __convert_name(self):
        self.__settings[self.__overrides["main"]] = \
            self.__settings[self.__overrides["main name"]]

        self.__settings.pop(self.__overrides["main name"])


class _SetupPluginDir(object):

    __LOGGER = logging.getLogger(__name__ + "._SetupPluginDir")

    def __init__(self):
        self.__loader = storage.Storage()

    def add_locations_from_settings(self, settings):
        # type: (Dict[str, Any]) -> None
        try:
            location = self.__get_location_from_settings(settings)
            self.__add_found_location(location)
        except KeyError:
            self.__LOGGER.info("No extra plugin directories found.")

    @staticmethod
    def __get_location_from_settings(settings):
        # type: (Dict[str, Dict[str, str]]) -> str
        return settings["Global Options"]["plugin directory"]

    def __add_found_location(self, location):
        # type: (str) -> None
        self.__loader.add_location(location)
        self.__LOGGER.info("Found extra plugin locations %s" % repr(location))


class Setup(object):

    def __init__(self):
        self.__settings = None

    def load_settings(self, settings_overrides, configuration_location):
        # type: (Dict[str, Any], str) -> None
        config = self.__load_config(configuration_location)
        internal = self.__internalize_settings(config, settings_overrides)
        self.__process_plugin_path(internal)
        self.__correct_settings(internal)

    @staticmethod
    def __load_config(configuration_location):
        # type: (str) -> Dict[str, Any]
        loader = _reader.ConfigurationLoader()
        return loader.read_config(configuration_location)

    @staticmethod
    def __internalize_settings(configuration, settings_overrides):
        # type: (Dict[str, Any], Dict[str, Any]) -> Dict[str, Any]
        internalize = _InternalizeSettings()
        return internalize.processed_settings(
            configuration, settings_overrides
        )

    @staticmethod
    def __process_plugin_path(settings):
        # type: (Dict[str, Any]) -> None
        plugin_dir = _SetupPluginDir()
        plugin_dir.add_locations_from_settings(settings)

    def __correct_settings(self, settings):
        # type: (Dict[str, Any]) -> None
        corrector = _correct_configuration.SettingsAid()
        self.__settings = corrector.correct_settings(settings)

    @property
    def loaded_settings(self):
        # type: () -> Dict[str, Any]
        return self.__settings

    @property
    def plugin_ids(self):
        # type: () -> List[str]
        return list(self.__settings.keys())
