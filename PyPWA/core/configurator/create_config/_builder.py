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
Creates the configuration
-------------------------

.. todo::
   Refactor this entire file.

- ConfigurationBuilder - Actually holds the questions being asked.

- _AskForSpecificPlugin - Handles selecting the plugin needed when there is 
  more than one plugin when it can.
  
- PluginList - Returns a list of all the plugins.
"""

import logging

import typing
import ruamel.yaml.comments

import PyPWA.builtin_plugins
import PyPWA.shell
from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import option_tools
from PyPWA.core.configurator import options
from PyPWA.core.configurator.create_config import _input
from PyPWA.core.configurator.storage import core_storage
from PyPWA.core.shared import plugin_loader


__credits__ = ["Mark Jones", "Ryan Wright"]
__author__ = AUTHOR
__version__ = VERSION


class ConfigurationBuilder(object):  # help, I am not simple
    __logger = logging.getLogger(__name__)
    __input_manager = _input.SimpleInputObject()
    __settings = ruamel.yaml.comments.CommentedMap()

    __plugin_handler = None  # type:

    __storage = None  # type: core_storage.MetadataStorage()
    __plugin_directory = None  # type: str
    __save_location = None  # type: str
    __level = None  # type: str
    __plugins = None  # type: list

    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())
        self.__plugin_handler = plugin_loader.PluginStorage()

    def build_configuration(
            self, plugin_name, main_plugin,
            provided_options=None, save_location=False
    ):
        self.__determine_plugin_level()
        self.__determine_plugin_directory()
        self.__build_storage()
        self.__make_plugin_list(main_plugin)
        self.__build_configuration()
        self.__add_main_to_configuration(main_plugin)
        self.__logger.debug("Settings: %s" % self.__settings)
        self.__correct_options(main_plugin, plugin_name, provided_options)
        self.__set_save_location(save_location)
        self.__write_final_config()

    def __determine_plugin_level(self):
        possible_levels = ["required", "optional", "advanced"]

        question = "\nHow much control would you like to have over the " \
                   "configuration? \nrequired\noptional (default, " \
                   "recommended)\nadvanced\n\n[optional]: "

        self.__level = self.__input_manager.input(
            question, possible_levels, "optional"
        )

    def __determine_plugin_directory(self):
        question = "\nWould you like to use your own plugins? If YES " \
                   "then please enter the location, if NO then just " \
                   "press ENTER.\n[None]: "

        if self.__level == "advanced":
            self.__plugin_directory = self.__input_manager.input(
                question, default_answer="None"
            )
        else:
            self.__plugin_directory = None

    def __build_storage(self):
        self.__plugin_handler.add_plugin_location(
            [PyPWA.builtin_plugins, self.__plugin_directory]
        )

        plugins = self.__plugin_handler.get_by_class(options.Plugin)

        self.__storage = core_storage.MetadataStorage()
        self.__storage.add_plugins(plugins)

    def __make_plugin_list(self, main_plugin):
        list_maker = PluginList(self.__storage)
        self.__plugins = list_maker.parse_plugins(main_plugin)

    def __build_configuration(self):
        configuration = ruamel.yaml.comments.CommentedMap()
        for plugin in self.__plugins:

            configuration.update()
        self.__settings = configuration

    def __add_main_to_configuration(self, main_plugin):
        self.__settings.update(main_plugin.option_difficulties)

    def __correct_options(self, main_plugin, main_name, provided_options):
        shell_id = main_plugin.plugin_name
        self.__settings[main_name] = self.__settings[shell_id]

        if provided_options:
            for option in provided_options:
                try:
                    self.__settings[shell_id].pop(option)
                except KeyError:
                    raise AttributeError(
                        "There is no option '{0}'!".format(option)
                    )

        self.__settings.pop(shell_id)

    def __set_save_location(self, save_location=False):
        question = "\nWhat would you like to name the configuration " \
                   "file?\nFile Name?: "

        if save_location:
            self.__save_location = save_location
        else:
            self.__save_location = self.__input_manager.input(question)

    def __write_final_config(self):

        with open(self.__save_location, "w") as stream:
            stream.write(
                ruamel.yaml.dump(
                    self.__settings, Dumper=ruamel.yaml.RoundTripDumper
                )
            )


class _AskForSpecificPlugin(object):
    __logger = logging.getLogger(__name__ + "._AskForSpecificPlugin")

    __names = None  # type: []
    __prettied_type = None  # type: str
    __question_string = None  # type: str
    __input_handler = None  # type: _input.SimpleInputObject()
    __plugin_prettier = None  # type: option_tools.PluginNameConversion

    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())
        self.__input_handler = _input.SimpleInputObject()

    def get_specific_plugin(self, plugin_list, plugin_type):
        self.__logger.debug("Found plugin_type: %s" % repr(plugin_type))
        self.__set_pretty_type(plugin_type)
        self.__set_names(plugin_list)
        self.__set_question_string()
        return self.__ask_the_question()

    def __set_pretty_type(self, plugin_type):
        prettier = option_tools.PluginNameConversion()
        self.__prettied_type = prettier.internal_to_external(plugin_type)

    def __set_names(self, plugin_list):
        names = []
        for plugin in plugin_list:
            names.append(self.__get_plugin_name(plugin))
        self.__names = names

    @staticmethod
    def __get_plugin_name(plugin):
        return plugin.plugin_name

    def __set_question_string(self):
        base_string = self.__format_base_string()
        name_string = self.__build_name_list()
        self.__question_string = base_string + name_string + "\nPlugin?: "

    def __format_base_string(self):
        base_string = "Which plugin would you like to use for {0}?"
        base_string = base_string.format(self.__prettied_type)
        self.__logger.debug("Parsed question: %s" % base_string)
        return base_string

    def __build_name_list(self):
        name_string = ""
        for name in self.__names:
            name_string += "\n{0}".format(name)
        return name_string

    def __ask_the_question(self):
        the_answer = self.__input_handler.input(
            self.__question_string, possible_answers=self.__names
        )
        return the_answer


class PluginList(object):

    __logger = logging.getLogger(__name__)
    __ask_for_plugin = _AskForSpecificPlugin()

    __storage = None  # type: core_storage.MetadataStorage()
    __plugin_types = None  # type: typing.List[str]

    def __init__(self, storage):
        self.__logger.addHandler(logging.NullHandler())
        self.__storage = storage
        self.__set_plugin_types()

    def __set_plugin_types(self):
        self.__plugin_types = options.Types

    def parse_plugins(self, main_plugin):
        plugins = []

        for plugin_type in self.__plugin_types:
            if plugin_type in main_plugin.required_plugins:
                plugins.append(self.__process_plugins(plugin_type))

        return plugins

    def __process_plugins(self, plugin_type):
        plugin_list = self.__storage.request_plugin_by_type(plugin_type)
        if self.__only_one_plugin(plugin_list):
            return plugin_list[0]()
        else:
            name = self.__ask_for_plugin.get_specific_plugin(
                plugin_list, plugin_type
            )

            empty_plugin = self.__storage.search_plugin(name, plugin_type)
            return empty_plugin()

    @staticmethod
    def __only_one_plugin(plugin_list):
        if len(plugin_list) == 1:
            return True
        else:
            return False
