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

import logging

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import options
from PyPWA.core.configurator.create_config import _builder
from PyPWA.core.configurator.create_config import _metadata
from PyPWA.core.configurator.create_config import _questions

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _GetPluginList(object):
    __logger = logging.getLogger(__name__)
    __ask_for_plugin = _questions.GetSpecificPlugin()
    __storage = _metadata.MetadataStorage()

    __plugin_list = None
    __main_plugin = None

    def __init__(self):
        self.__plugin_list = []

    def parse_plugins(self, main_plugin):
        for plugin_type in options.Types:
            if plugin_type in main_plugin.required_plugins:
                self.__plugin_list.append(self.__process_plugins(plugin_type))
        self.__main_plugin = main_plugin

    def __process_plugins(self, plugin_type):
        plugin_list = self.__storage.request_plugins_by_type(plugin_type)
        if self.__only_one_plugin(plugin_list):
            return plugin_list[0]
        else:
            self.__ask_for_plugin.ask_for_plugin(plugin_list, plugin_type)
            name = self.__ask_for_plugin.get_specific_plugin()

            empty_plugin = self.__storage.search_plugin(name, plugin_type)
            return empty_plugin

    @staticmethod
    def __only_one_plugin(plugin_list):
        if len(plugin_list) == 1:
            return True
        else:
            return False

    @property
    def plugins(self):
        return self.__plugin_list

    @property
    def shell(self):
        return self.__main_plugin


class StartConfig(object):

    __storage = _metadata.MetadataStorage()
    __plugin_dir = _questions.GetPluginDirectory()
    __level = _questions.GetPluginLevel()
    __save_location = _questions.GetSaveLocation()
    __plugin_list = _GetPluginList()
    __configuration = _builder.BuildConfig(__plugin_list, __level)

    __main_plugin = None

    def make_config(self, function_settings, config_location):
        self.__fetch_main_plugin(function_settings)
        self.__get_plugin_directories()
        self.__set_level()
        self.__set_plugin_list()
        self.__set_save_location(config_location)

    def __fetch_main_plugin(self, function_settings):
        self.__main_plugin = self.__storage.request_main_plugin_by_name(
            function_settings["main"]
        )

    def __get_plugin_directories(self):
        self.__plugin_dir.ask_for_plugin_directory()
        self.__storage.add_location(self.__plugin_dir.get_plugin_directory())

    def __set_level(self):
        self.__level.ask_for_plugin_level()

    def __set_plugin_list(self):
        self.__plugin_list.parse_plugins(self.__main_plugin)

    def __set_save_location(self, save_location):
        if save_location:
            self.__save_location.override_save_location(save_location)
        else:
            self.__save_location.ask_for_save_location()

    def __create_configuration(self, function_settings):
        self.__configuration.build(function_settings)

    def __save_configuration(self):
        print("Cause I've already done a lot.")
        print(self.__configuration.configuration)
