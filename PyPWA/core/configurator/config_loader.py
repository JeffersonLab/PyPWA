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

"""

"""

import io
import logging
import os
import sys

import PyPWA.builtin_plugins
import PyPWA.shell
import fuzzywuzzy.process
import ruamel.yaml
import ruamel.yaml.comments
import ruamel.yaml.parser
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core import plugin_loader
from PyPWA.core.configurator import _storage
from PyPWA.core.templates import option_templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ConfigParser(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    def read_config(self, configuration):
        with open(configuration, "r") as stream:
            return self._process_stream(stream)

    def _process_stream(self, stream):
        try:
            return self._load_configuration(stream)
        except ruamel.yaml.parser.ParserError as UserError:
            self._process_error(UserError)

    @staticmethod
    def _load_configuration(stream):
        return ruamel.yaml.load(stream, ruamel.yaml.RoundTripLoader)

    def _process_error(self, user_error):
        self._logger.exception(user_error)
        raise SyntaxError(str(user_error))


class SimpleConfigBuilder(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        self._plugin_handler = plugin_loader.PluginLoading(
            option_templates.PluginsOptionsTemplate
        )

        self._input_manager = SimpleInputObject()
        self._settings = ruamel.yaml.comments.CommentedMap()

        self._storage = None  # type: _storage.MetadataStorage
        self._plugin_directory = None  # type: str
        self._save_location = None  # type: str
        self._level = None  # type: str
        self._plugins = None  # type: list

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
        plugins = self._plugin_handler.fetch_plugin(
            [PyPWA.builtin_plugins, self._plugin_directory]
        )

        self._storage = _storage.MetadataStorage()
        self._storage.add_plugins(plugins)

    def _make_plugin_list(self, main_plugin):
        list_maker = PluginList()
        self._plugins = list_maker.parse_plugins(
            main_plugin, self._storage
        )

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


class PluginList(object):

    def __init__(self):
        """

        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        self._input_manager = SimpleInputObject()

    def parse_plugins(self, main_plugin, storage):
        """

        Args:
            main_plugin:
            storage:

        Returns:

        """
        plugins = []
        if main_plugin.requires("data parser"):
            plugins.append(self._process_plugins(
                "data parser", "Data Parsing", storage,
                storage.data_parser
            ))

        if main_plugin.requires("data reader"):
            plugins.append(self._process_plugins(
                "data reader", "Data Iterator", storage,
                storage.data_reader
            ))

        if main_plugin.requires("kernel processing"):
            plugins.append(self._process_plugins(
                "kernel processing", "Kernel Processor", storage,
                storage.kernel_processing
            ))

        if main_plugin.requires("minimization"):
            plugins.append(self._process_plugins(
                "minimization", "Minimizer", storage,
                storage.minimization
            ))

        return plugins

    def _process_plugins(
            self, plugin_type, plugin_type_name, storage, plugin_list
    ):
        """

        Args:
            plugin_type:
            plugin_type_name:
            storage:
            plugin_list:

        Returns:

        """
        if len(plugin_list) == 1:
            empty_plugin = plugin_list[0]
        else:
            name = self._ask_plugin(
                plugin_list, plugin_type_name
            )

            empty_plugin = storage.search_plugin(name, plugin_type)

        return empty_plugin()

    def _ask_plugin(self, plugin_list, plugin_type):
        """

        Args:
            plugin_list:
            plugin_type:

        Returns:

        """
        names = []
        for plugin in plugin_list:
            the_plugin = plugin()
            names.append(the_plugin.request_metadata("name"))

        string = "Which would plugin would you " \
                 "like to use for {0}?".format(plugin_type)

        for name in names:
            string += "\n{0}".format(name)

        string += "\nPlugin?: "

        return self._input_manager.input(string, possible_answers=names)
