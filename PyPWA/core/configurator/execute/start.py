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
Where the program really starts.
--------------------------------
Here is where the plugins are loaded, passed their options, and then passed 
to the main objects.

- SetupSettings - Corrects the settings and setups the storage module.

- SetupPlugins - Initializes the correct plugins, passes them along with 
  needed options to the main, then starts the program.
"""

import logging

import typing

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import option_tools
from PyPWA.core.configurator.execute import _correct_settings_values
from PyPWA.core.configurator.execute import config_loader
from PyPWA.core.configurator.storage import module_fetcher
from PyPWA.core.configurator.storage import template_parser
from PyPWA.core.shared.interfaces import plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class SetupSettings(object):

    __config_parser = config_loader.ConfigurationLoader()
    __storage = None  # type: module_fetcher.ModulePicking
    __extra_plugins = None  # type: str
    __parsed_config = None  # type: dict
    __corrected_settings = None  # type: dict

    def run(self, function_settings, configuration_location):
        self.__load_config(configuration_location)
        self.__process_extra_options(function_settings)
        self.__convert_name(function_settings)
        self.__set_storage()
        self.__correct_settings()
        self.__execute()

    def __load_config(self, config):
        self.__parsed_config = self.__config_parser.read_config(config)

    def __process_extra_options(self, function_settings):
        try:
            self.__set_main_name(function_settings)
        except KeyError:
            pass

        try:
            self.__set_plugin_directory()
        except KeyError:
            pass

    def __set_main_name(self, function_settings):
        for key in list(function_settings["main options"].keys()):
            self.__parsed_config[function_settings["main name"]][key] = \
                function_settings["main options"][key]

    def __set_plugin_directory(self):
        self.__extra_plugins = \
            self.__parsed_config["Global Options"]["plugin directory"]

    def __convert_name(self, function_settings):
        self.__parsed_config[function_settings["main"]] = \
            self.__parsed_config[function_settings["main name"]]
        self.__parsed_config.pop(function_settings["main name"])

    def __set_storage(self):
        self.__storage = module_fetcher.ModulePicking(self.__extra_plugins)

    def __correct_settings(self):
        template_loader = template_parser.TemplateLoader(
            self.__extra_plugins
        )
        settings_aid = _correct_settings_values.SettingsAid(
            template_loader.templates
        )
        self.__corrected_settings = settings_aid.correct_settings(
            self.__parsed_config
        )

    def __execute(self):
        main = SetupPlugins(self.__storage, self.__correct_settings)
        main.start()


class SetupPlugins(object):
    __logger = logging.getLogger(__name__)

    __settings = None  # type: dict
    __plugin_storage = None  # type: module_fetcher.ModulePicking
    __plugin_ids = None  # type: typing.List[str]
    __main_plugin = None  # type: plugins.ShellMain()
    __selected_plugins = None  # type: typing.List[typing.Any]
    __initialized_plugins = None  # type: dict
    __initialized_shell = None  # type: typing.Any

    def __init__(self, plugin_storage, settings):
        self.__logger.addHandler(logging.NullHandler())
        self.__initialize_variables()

        self.__plugin_storage = plugin_storage
        self.__settings = settings

    def __initialize_variables(self):
        self.__plugin_ids = []
        self.__selected_plugins = []
        self.__initialized_plugins = {}

    def start(self):
        self.__set_plugin_ids()
        self.__load_plugins()
        self.__load_main()
        self.__setup_plugins()
        self.__setup_shell()
        self.__start()

    def __set_plugin_ids(self):
        self.__plugin_ids = list(self.__settings.keys())

    def __load_plugins(self):
        for the_id in self.__plugin_ids:
            temp = self.__plugin_storage.request_plugin_by_name(the_id)
            if temp:
                self.__selected_plugins.append(temp)

    def __load_main(self):
        for the_id in self.__plugin_ids:
            temp = self.__plugin_storage.request_main_by_id(the_id)
            if temp:
                self.__logger.debug("Found: " + repr(temp))
                self.__main_plugin = temp

    def __setup_plugins(self):
        for plugin in self.__selected_plugins:
            self.__process_plugin(plugin)

    def __process_plugin(self, plugin):
        command = self.__get_command_object(plugin.plugin_name)
        interface = self.__get_interface(plugin, command)
        self.__initialized_plugins[plugin.provides] = interface

    def __get_command_object(self, name):
        plugin_setting = self.__settings[name]
        command = option_tools.CommandOptions(plugin_setting)
        return command

    @staticmethod
    def __get_interface(plugin, command):
        setup = plugin.setup(command)
        interface = setup.return_interface()
        return interface

    def __setup_shell(self):
        main_settings = self.__settings[self.__main_plugin.plugin_name]
        self.__logger.debug("Found settings: " + repr(main_settings))
        main_command = option_tools.CommandOptions(main_settings)
        shell = self.__main_plugin.setup(main_command)
        self.__initialized_shell = shell()

    def __start(self):
        self.__initialized_shell.start()
