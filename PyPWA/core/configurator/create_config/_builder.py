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
    _logger = logging.getLogger(__name__)
    _input_manager = _input.SimpleInputObject()
    _settings = ruamel.yaml.comments.CommentedMap()

    _plugin_handler = None  # type:

    _storage = None  # type: _storage.MetadataStorage()
    _plugin_directory = None  # type: str
    _save_location = None  # type: str
    _level = None  # type: str
    _plugins = None  # type: list

    def __init__(self):
        self._logger.addHandler(logging.NullHandler())

        self._plugin_handler = plugin_loader.PluginStorage()

    def build_configuration(
            self, plugin_name, main_plugin,
            provided_options=None, save_location=False
    ):
        self._determine_plugin_level()
        self._determine_plugin_directory()
        self._build_storage()
        self._make_plugin_list(main_plugin)
        self._build_configuration()
        self._add_main_to_configuration(main_plugin)
        self._correct_options(main_plugin, plugin_name, provided_options)
        self._set_save_location(save_location)
        self._write_final_config()

    def _determine_plugin_level(self):
        possible_levels = ["required", "optional", "advanced"]

        question = "\nHow much control would you like to have over the " \
                   "configuration? \nrequired\noptional (default, " \
                   "recommended)\nadvanced\n\n[optional]: "

        self._level = self._input_manager.input(
            question, possible_levels, "optional"
        )

    def _determine_plugin_directory(self):
        question = "\nWould you like to use your own plugins? If YES " \
                   "then please enter the location, if NO then just " \
                   "press ENTER.\n[None]: "

        if self._level == "advanced":
            self._plugin_directory = self._input_manager.input(
                question, default_answer="None", is_dir=True
            )
        else:
            self._plugin_directory = None

    def _build_storage(self):
        self._plugin_handler.add_plugin_location(
            [PyPWA.builtin_plugins, self._plugin_directory]
        )

        plugins = self._plugin_handler.get_by_class(options.Plugin)

        self._storage = core_storage.MetadataStorage()
        self._storage.add_plugins(plugins)

    def _make_plugin_list(self, main_plugin):
        list_maker = PluginList(self._storage)
        self._plugins = list_maker.parse_plugins(main_plugin)

    def _build_configuration(self):
        configuration = ruamel.yaml.comments.CommentedMap()
        for plugin in self._plugins:
            configuration.update(plugin.request_options(self._level))
        self._settings = configuration

    def _add_main_to_configuration(self, main_plugin):
        self._settings.update(main_plugin.request_options(self._level))

    def _correct_options(
            self, main_plugin, main_name, provided_options
    ):
        shell_id = main_plugin.request_metadata("id")

        if provided_options:
            for option in provided_options:
                try:
                    self._settings[shell_id].pop(option)
                except KeyError:
                    raise AttributeError(
                        "There is no option '{0}'!".format(option)
                    )

        self._settings[main_name] = self._settings[shell_id]
        self._settings.pop(shell_id)

    def _set_save_location(self, save_location=False):
        question = "\nWhat would you like to name the configuration " \
                   "file?\nFile Name?: "

        if save_location:
            self._save_location = save_location
        else:
            self._save_location = self._input_manager.input(question)

    def _write_final_config(self):

        with open(self._save_location, "w") as stream:
            stream.write(
                ruamel.yaml.dump(
                    self._settings, Dumper=ruamel.yaml.RoundTripDumper
                )
            )


class _AskForSpecificPlugin(object):
    __logger = logging.getLogger(__name__ + "._AskForSpecificPlugin")

    _names = None  # type: []
    _prettied_type = None  # type: str
    _question_string = None  # type: str
    _input_handler = None  # type: _input.SimpleInputObject()
    _plugin_prettier = None  # type: option_tools.PluginNameConversion

    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())
        self._input_handler = _input.SimpleInputObject()

    def get_specific_plugin(self, plugin_list, plugin_type):
        self.__logger.debug("Found plugin_type: %s" % repr(plugin_type))
        self._set_pretty_type(plugin_type)
        self._set_names(plugin_list)
        self._set_question_string()
        return self._ask_the_question()

    def _set_pretty_type(self, plugin_type):
        prettier = option_tools.PluginNameConversion()
        self._prettied_type = prettier.internal_to_external(plugin_type)

    def _set_names(self, plugin_list):
        names = []
        for plugin in plugin_list:
            names.append(self._get_plugin_name(plugin))
        self._names = names

    @staticmethod
    def _get_plugin_name(plugin):
        return plugin.plugin_name

    def _set_question_string(self):
        base_string = self._format_base_string()
        name_string = self._build_name_list()
        self._question_string = base_string + name_string + "\nPlugin?: "

    def _format_base_string(self):
        base_string = "Which plugin would you like to use for {0}?"
        base_string.format(self._prettied_type)
        return base_string

    def _build_name_list(self):
        name_string = ""
        for name in self._names:
            name_string += "\n{0}".format(name)
        return name_string

    def _ask_the_question(self):
        the_answer = self._input_handler.input(
            self._question_string, possible_answers=self._names
        )
        return the_answer


class PluginList(object):

    _logger = logging.getLogger(__name__)
    _ask_for_plugin = _AskForSpecificPlugin()

    _storage = None  # type: _storage.MetadataStorage()
    _plugin_types = None  # type: [str]

    def __init__(self, storage):
        self._logger.addHandler(logging.NullHandler())
        self._storage = storage
        self._set_plugin_types()

    def _set_plugin_types(self):
        self._plugin_types = options.Types

    def parse_plugins(self, main_plugin):
        plugins = []

        for plugin_type in self._plugin_types:
            if plugin_type in main_plugin.required_plugins:
                plugins.append(self._process_plugins(plugin_type))

        return plugins

    def _process_plugins(self, plugin_type):
        plugin_list = self._storage.request_plugin_by_type(plugin_type)
        if self._only_one_plugin(plugin_list):
            return plugin_list[0]()
        else:
            name = self._ask_for_plugin.get_specific_plugin(
                plugin_list, plugin_type
            )

            empty_plugin = self._storage.search_plugin(name, plugin_type)
            return empty_plugin()

    @staticmethod
    def _only_one_plugin(plugin_list):
        if len(plugin_list) == 1:
            return True
        else:
            return False
