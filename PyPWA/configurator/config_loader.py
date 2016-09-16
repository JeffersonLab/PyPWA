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
import sys

import PyPWA.libs
import PyPWA.shell
import fuzzywuzzy.process
import io
import os
import ruamel.yaml
import ruamel.yaml.parser
import ruamel.yaml.comments
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.configurator import _storage
from PyPWA.core_libs import plugin_loader
from PyPWA.core_libs.templates import option_templates

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
        """
        Parses the configuration that the user specified.

        Args:
            configuration (str): The name of the configuration file.

        Returns:
            dict: The configuration of the program.
        """
        # Using the word 'unclean' is hip, right?
        return self._parse_config(configuration)

    def _parse_config(self, configuration):
        """
        Reads in the configuration file into memory then returns the
        unfiltered dictionary.
            If there is a syntax error it will catch the error then raise
        a cleaned version of the error to not flood the user with
        unneeded information.
            The full exception will be passed to the logger if the user
        wants to see the full error, should only show if they have
        verboseness enabled.

        Args:
            configuration (str): The name of the configuration file.

        Returns:
            dict: The unfiltered dictionary of the configuration.

        Raises:
            SyntaxError: If there is a typo or other similar error in the
                configuration file.
        """
        with io.open(configuration, "r") as stream:
            try:
                return ruamel.yaml.load(
                    stream, ruamel.yaml.RoundTripLoader
                )
            except ruamel.yaml.parser.ParserError as UserError:
                self._logger.exception(UserError)
                raise SyntaxError(str(UserError))


class MakeConfiguration(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        self._plugin_handler = plugin_loader.PluginLoading(
            option_templates.PluginsOptionsTemplate
        )

        self._input_manager = SimpleInputObject()

        self._settings = {}

        self._save_location = ""
        self._level = ""

    def make_configuration(
            self, plugin_name, main_plugin,
            provided_options=None, save_location=""
    ):
        """

        Args:
            plugin_name (str):
            main_plugin (option_templates.MainOptionsTemplate):
            provided_options (list):
            save_location (str):

        Returns:

        """
        plugin_directory = None

        self._save_location = save_location
        self._request_level()
        if self._level == "advanced":
            plugin_directory = self._request_plugin()

        plugins = self._plugin_handler.fetch_plugin(
            [PyPWA.libs, plugin_directory]
        )

        storage = _storage.MetadataStorage()
        storage.add_plugins(plugins)

        selected_plugins = self._parse_plugins(main_plugin, storage)
        configuration = self._build_configuration(selected_plugins)
        full_configuration = self._add_main_plugin_to_configuration(
            configuration, main_plugin
        )

        fixed_config = self._correct_main_name(
            main_plugin, plugin_name, full_configuration, provided_options
        )

        self._write_config(fixed_config)

    def _add_main_plugin_to_configuration(
            self, configuration, main_plugin
    ):
        configuration[main_plugin.request_metadata("id")] = \
            main_plugin.request_options(self._level)

        return configuration

    def _write_config(self, configuration):
        string = """\
What would you like to name the configuration file?
[File Name?]: """

        if self._save_location == "":
            self._save_location = self._input_manager.input(string)

        with io.open(self._save_location, "w") as stream:
            stream.write(
                ruamel.yaml.dump(
                    configuration,
                    Dumper=ruamel.yaml.RoundTripDumper
                )
            )

    @staticmethod
    def _correct_main_name(
            main_plugin, main_name, configuration, provided_options=None
    ):
        """

        Args:
            main_plugin (option_templates.MainOptionsTemplate):
            main_name (str):
            configuration (dict):

        Returns:

        """
        shell_id = main_plugin.request_metadata("id")

        if provided_options:
            for option in provided_options:
                configuration[shell_id].pop(option)

        configuration[main_name] = \
            configuration[shell_id]

        configuration.pop(shell_id)

        return configuration

    def _build_configuration(self, plugin_list):
        """

        Args:
            plugin_list (list[option_templates.PluginsOptionsTemplate]):

        Returns:

        """
        configuration = ruamel.yaml.comments.CommentedMap()
        for plugin in plugin_list:
            configuration.update(plugin.request_options(self._level))

        return configuration

    def _parse_plugins(self, main_plugin, storage):
        """

        Args:
            main_plugin (option_templates.MainOptionsTemplate):
            storage (_storage.MetadataStorage):

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
            plugin_type (str):
            plugin_type_name (str):
            storage (_storage.MetadataStorage):
            plugin_list (list):

        Returns:

        """

        if len(plugin_list) == 1:
            empty_plugin = plugin_list[0]
        else:
            name = self._ask_plugin(
                storage.data_parser, plugin_type_name
            )

            empty_plugin = storage.search_plugin(name, plugin_type)

        return empty_plugin()

    def _ask_plugin(self, plugin_list, plugin_type):
        """

        Args:
            plugin_list (list[option_templates.PluginsOptionsTemplate]):

        Returns:

        """
        names = []
        for plugin in plugin_list:
            names.append(plugin.request_metadata("name"))

        string = """\
Which would plugin would you like to use for {0}?
""".format(plugin_type)

        for name in names:
            string += "\n{0}".format(name)

        string += "\nPlugin?: "

        return self._input_manager.input(string, possible_answers=names)

    def _request_plugin(self):
        string = """
Would you like to use your own plugins? If YES then please enter the
location, if NO then just press ENTER.
[None]: """

        return self._input_manager.input(string, is_dir=True)

    def _request_level(self):
        string = """\
How much control would you like to have over the configuration?
required
optional (default, recommended)
advanced

[optional]: """

        levels = ["required", "optional", "advanced"]

        self._level = self._input_manager.input(
            string, possible_answers=levels, default_answer="optional"
        )


class SimpleInputObject(object):

    def __init__(self, auto_correct_percentage=75):
        if sys.version_info.major == "2":
            self.__input = raw_input
        else:
            self.__input = input

        self._auto_correction_percentage = auto_correct_percentage

    def input(
            self, string, possible_answers=False,
            default_answer=False, is_dir=False
    ):
        """

        Args:
            string (str):
            possible_answers (list):
            default_answer (str):
            is_dir (bool):

        Returns:

        """
        final_answer = False

        while not final_answer:
            answer = self.__input(string)

            if answer is "" and default_answer:
                final_answer = default_answer
                continue

            else:
                if possible_answers:
                    corrected_answer = fuzzywuzzy.process.extractOne(
                        answer, possible_answers
                    )

                    if corrected_answer[1] > \
                            self._auto_correction_percentage:
                        answer = corrected_answer[0]

                if is_dir:
                    if not os.path.isdir(answer):
                        continue
                if self._is_correct(answer):
                    final_answer = answer

        return final_answer

    def _is_correct(self, answer):
        final_answer = False
        string = """\
It looks like you selected '{0}', is this correct?
[Y]es/No: """

        while not final_answer:
            is_correct = self.__input(string.format(answer))

            value = fuzzywuzzy.process.extractOne(
                is_correct.lower(), ["yes", "no"]
            )

            if value[1] > self._auto_correction_percentage:
                if value[0] == "yes":
                    final_answer = "yes"
                else:
                    final_answer = "no"

        if final_answer == "yes":
            return True
        elif final_answer == "no":
            return False