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

- ConfigurationLoader - Simply loads the configuration file using ruamel.yaml.

- _InternalizeSettings - Takes the settings loaded from the configuration, 
  and replaces select keys in the configuration with keys from the settings 
  override in the entry function. Useful so that you can have multiple names
  for the same main module.
  
- _SetupPluginDir - Pulls the plugin directory from the configuration and 
  adds the path to the storage objects plugin search path.
  
- Setup - Takes the configuration and override information then parses that 
  information into a usable configuration dictionary.
"""

import logging

import ruamel.yaml
import ruamel.yaml.parser

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import storage
from PyPWA.core.configurator.execute import _correct_configuration

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _ConfigurationLoader(object):

    __logger = logging.getLogger(__name__ + ".ConfigurationLoader")

    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())

    def read_config(self, configuration):
        with open(configuration, "r") as stream:
            return self.__process_stream(stream)

    def __process_stream(self, stream):
        try:
            return self.__load_configuration(stream)
        except ruamel.yaml.parser.ParserError as UserError:
            self.__process_error(UserError)

    @staticmethod
    def __load_configuration(stream):
        return ruamel.yaml.load(stream, ruamel.yaml.RoundTripLoader)

    def __process_error(self, user_error):
        self.__logger.exception(user_error)
        raise SyntaxError(str(user_error))


class _InternalizeSettings(object):

    __logger = logging.getLogger(__name__ + "._InternalizeSettings")
    __settings = None
    __overrides = None

    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())

    def processed_settings(self, settings, settings_overrides):
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
            self.__logger.debug("Failed to find main options")

    def __process_overrides(self):
        for key in self.__overrides["main options"]:
            self.__settings[self.__overrides["main name"]][key] = \
                self.__overrides["main options"][key]

    def __convert_name(self):
        self.__settings[self.__overrides["main"]] = \
            self.__settings[self.__overrides["main name"]]

        self.__settings.pop(self.__overrides["main name"])


class _SetupPluginDir(object):

    __logger = logging.getLogger(__name__ + "._SetupPluginDir")
    __loader = storage.Storage()

    def add_locations_from_settings(self, settings):
        try:
            location = self.__get_location_from_settings(settings)
            self.__add_found_location(location)
        except KeyError:
            self.__logger.info("No extra plugin directories found.")

    @staticmethod
    def __get_location_from_settings(settings):
        return settings["Global Options"]["plugin directory"]

    def __add_found_location(self, location):
        self.__loader.add_location(location)
        self.__logger.info("Found extra plugin locations %s" % repr(location))


class Setup(object):

    __settings = None

    def load_settings(self, settings_overrides, configuration_location):
        config = self.__load_config(configuration_location)
        internal = self.__internalize_settings(config, settings_overrides)
        self.__process_plugin_path(internal)
        self.__correct_settings(internal)

    @staticmethod
    def __load_config(configuration_location):
        loader = _ConfigurationLoader()
        return loader.read_config(configuration_location)

    @staticmethod
    def __internalize_settings(configuration, settings_overrides):
        internalize = _InternalizeSettings()
        return internalize.processed_settings(
            configuration, settings_overrides
        )

    @staticmethod
    def __process_plugin_path(settings):
        plugin_dir = _SetupPluginDir()
        plugin_dir.add_locations_from_settings(settings)

    def __correct_settings(self, settings):
        corrector = _correct_configuration.SettingsAid()
        self.__settings = corrector.correct_settings(settings)

    @property
    def loaded_settings(self):
        return self.__settings

    @property
    def plugin_ids(self):
        return list(self.__settings.keys())
