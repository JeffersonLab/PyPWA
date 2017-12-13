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
Creates the template configuration file when --WriteConfig is passed
"""

from typing import Any, Dict

from PyPWA import AUTHOR, VERSION
from PyPWA.initializers.configurator.create_config import _builder
from PyPWA.initializers.configurator.create_config import _function_builder
from PyPWA.initializers.configurator.create_config import _metadata
from PyPWA.initializers.configurator.create_config import _questions
from PyPWA.initializers.configurator.create_config import _writer

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class StartConfig(object):

    def __init__(self):
        self.__writer = _writer.Write()
        self.__functions = _function_builder.FunctionHandler()
        self.__storage = _metadata.MetadataStorage()
        self.__plugin_dir = _questions.GetPluginDirectory()
        self.__level = _questions.GetPluginLevel()
        self.__save_location = _questions.GetSaveLocation()
        self.__plugin_list = _metadata.GetPluginList()
        self.__configuration = _builder.BuildConfig(
            self.__plugin_dir, self.__plugin_list, self.__level
        )
        self.__main_plugin = None

    def make_config(self, function_settings, config_location):
        # type: (Dict[str, Any], str) -> None
        self.__fetch_main_plugin(function_settings)
        self.__get_plugin_directories()
        self.__set_level()
        self.__set_plugin_list()
        self.__create_configuration(function_settings)
        self.__set_save_location(config_location)
        self.__save_configuration()
        self.__save_functions()

    def __fetch_main_plugin(self, function_settings):
        # type: (Dict[str, Any]) -> None
        self.__main_plugin = self.__storage.request_program_by_name(
            function_settings["main"]
        )

    def __get_plugin_directories(self):
        self.__plugin_dir.ask_for_plugin_directory()
        self.__storage.add_location(self.__plugin_dir.get_plugin_directory())

    def __set_level(self):
        self.__level.ask_for_plugin_level()

    def __set_plugin_list(self):
        self.__plugin_list.parse_plugins(self.__main_plugin)

    def __create_configuration(self, function_settings):
        # type: (Dict[str, Any]) -> None
        self.__configuration.build(function_settings)

    def __set_save_location(self, save_location):
        # type: (str) -> None
        if save_location:
            self.__save_location.override_save_location(save_location)
        else:
            self.__save_location.ask_for_save_location()

    def __save_configuration(self):
        self.__writer.write(
            self.__configuration.configuration,
            self.__save_location.get_save_location()
        )

    def __save_functions(self):
        self.__functions.output_functions(
            self.__plugin_list, self.__save_location.get_save_location()
        )
