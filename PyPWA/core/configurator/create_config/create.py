#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

import PyPWA.shell
from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import options
from PyPWA.core.configurator.create_config import _builder
from PyPWA.core.shared import plugin_loader

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Config(object):

    __config_maker = _builder.ConfigurationBuilder()
    __logger = logging.getLogger(__name__ + ".Config")
    __loader = plugin_loader.PluginStorage()

    __main_plugin = None
    __settings = None
    __shell_name = None  # type: str
    __shell_id = None  # type: str
    __potential_plugins = None

    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())
        self.__setup_loader()

    def __setup_loader(self):
        self.__loader.add_plugin_location(PyPWA.shell)

    def make_config(self, function_settings, config_location):
        self.__process_function_settings(function_settings)
        self.__log_names()
        self.__load_potential_plugins()
        self.__search_for_main_plugin()
        self.__check_found_main()
        self.__create_configuration(config_location)

    def __process_function_settings(self, function_settings):
        self.__shell_id = function_settings["main"]
        self.__shell_name = function_settings["main name"]
        if "main options" in function_settings:
            self.__settings = function_settings["main options"]

    def __log_names(self):
        self.__logger.debug("Searching for ID: %s" % self.__shell_id)
        self.__logger.debug("Searching for name: %s" % self.__shell_name)

    def __load_potential_plugins(self):
        self.__potential_plugins = self.__loader.get_by_class(options.Main)

    def __search_for_main_plugin(self):
        for plugin in self.__potential_plugins:
            temp_object = plugin()
            if temp_object.plugin_name == self.__shell_id:
                self.__main_plugin = temp_object
                break

    def __check_found_main(self):
        if isinstance(self.__main_plugin, type(None)):
            raise RuntimeError(
                "Could not find the main object %s!" % self.__shell_name
            )

    def __create_configuration(self, config_location):
        self.__config_maker.build_configuration(
            self.__main_plugin, self.__main_plugin, self.__settings,
            config_location
        )
