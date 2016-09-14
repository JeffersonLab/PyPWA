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
import numpy
import os
import ruamel.yaml
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core_libs import plugin_loader
from PyPWA.core_libs.templates import option_templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


FUZZY_STRING_CONFIDENCE_LEVEL = 75  # percent from 0 to 100

if sys.version_info.major == 2:
    input = raw_input


class SettingsAid(object):

    _failed = "failed to find"

    def __init__(self):
        """
        Object that corrects the settings of the dictionaries rendered
        in from the user.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    def correct_settings(self, value, correct):
        """
        Corrects the settings of the dictionary using a template
        dictionary.

        Args:
            value (dict): Users dictionary.
            correct (dict): Template dictionary

        Returns:
            dict: The corrected dictionary.
        """
        key_correct_dictionary = self._correct_keys(value, correct)
        return self._correct_all(key_correct_dictionary, correct)

    def _correct_all(self, dictionary, template_dictionary):
        """
        Corrects all settings types.

        Args:
            dictionary (dict): The users dictionary.
            template_dictionary (dict): The Template dictionary.

        Returns:
            dict: The corrected dictionary.
        """
        corrected_dictionary = {}
        for key in dictionary.keys():
            template_value = template_dictionary[key]
            current_value = dictionary[key]

            if template_value == int:
                corrected_dictionary[key] = self._correct_integers(
                    current_value
                )

            elif template_value == float:
                corrected_dictionary[key] = self._correct_floats(
                    current_value
                )

            elif template_value == bool:
                corrected_dictionary[key] = self._correct_boolean_values(
                    current_value
                )

            elif template_value == str:
                corrected_dictionary[key] = str(current_value)

            elif template_value == list:
                corrected_dictionary[key] = list(current_value)

            elif template_value == set:
                corrected_dictionary[key] = set(current_value)

            elif isinstance(template_value, list):
                corrected_dictionary[key] = self._correct_from_list(
                    current_value, template_value
                )

            elif isinstance(template_value, dict):
                corrected_dictionary[key] = self.correct_settings(
                    current_value, template_value
                )

            else:
                self._logger.debug(
                    "Key {0} is not correctable by settings "
                    "aid.".format(key)
                )

                corrected_dictionary[key] = current_value

        return corrected_dictionary

    def _correct_keys(self, dictionary, template_dictionary):
        """
        Simple method that corrects only the keys in the dictionary.

        Args:
            dictionary (dict): The users dictionary
            template_dictionary (dict): The correct template dictionary.

        Returns:
            dict: The dictionary with the corrected keys.
        """
        key_correct_dict = {}
        correct_keys = list(template_dictionary.keys())

        for key in dictionary.keys():
            potential_key = fuzzywuzzy.process.extractOne(
                key, correct_keys
            )

            if potential_key[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
                key_correct_dict[potential_key[0]] = dictionary[key]

            else:
                self._logger.warning(
                    "Unknown key {0}, value is being "
                    "removed!".format(key)
                )

        return key_correct_dict

    def _correct_from_list(self, string, value_list):
        """
        Corrects a string using predefined strings inside a list.

        Args:
            string (str): The users string
            value_list (list): The potential values.

        Returns:
            str: The corrected values.
        """
        value = fuzzywuzzy.process.extractOne(string, value_list)

        if value[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
            return value[0]
        else:
            return self._failed

    def _correct_boolean_values(self, value):
        """
        Takes boolean values and translates them to Python Booleans.

        Args:
            value (str): The users supplied value.

        Returns:
            bool: The correct boolean.
        """
        try:
            exact = int(value)
            if exact:
                return True
            else:
                return False
        except ValueError:
            pass

        value = fuzzywuzzy.process.extractOne(value, ["true", "false"])
        if value[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
            if value[0] == "true":
                return True
            elif value[0] == "false":
                return False
            else:
                return self._failed
        else:
            return self._failed

    def _correct_integers(self, value):
        """
        Corrects integers read in to actual integers.

        Args:
            value (str): The string of the number.

        Returns:
            int: The correct value.
        """
        try:
            return int(value)
        except ValueError:
            return self._failed

    def _correct_floats(self, value):
        """
        Corrects the floats to numpy.float64s.

        Args:
            value (str): The users float.

        Returns:
            numpy.float64: The corrected value.
        """
        try:
            return numpy.float64(value)
        except ValueError:
            return self._failed


class PluginStorage(object):

    def __init__(self, extra_locations=None):
        plugins = [PyPWA.libs, PyPWA.shell]

        if isinstance(extra_locations, str):
            plugins.append(extra_locations)
        elif isinstance(extra_locations, list):
            for plugin in extra_locations:
                plugins.append(plugin)

        options_loader = plugin_loader.PluginLoading(
            option_templates.PluginsOptionsTemplate
        )

        shell_loader = plugin_loader.PluginLoading(
            option_templates.MainOptionsTemplate
        )

        self._plugins = options_loader.fetch_plugin(plugins)
        self._shell = shell_loader.fetch_plugin(plugins)

        templates = {}
        for plugin in self._plugins:
            templates[plugin.request_metadata("name")] = \
                plugin.request_options("template")

        for main in self._shell:
            templates[main.request_metadata("id")] = \
                main.request_options("template")

        self._templates = templates

    def request_main_by_id(self, the_id):
        """

        Args:
            the_id (str):

        Returns:

        """
        for main in self._shell:
            if main.request_metadata("id") == the_id:
                return main
        return False

    def request_plugin_by_name(self, name):
        for plugin in self._plugins:
            if plugin.request_metadata("name") == name:
                return plugin
        return False

    @property
    def templates_config(self):
        return self._templates


class MetadataStorage(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._minimization = []
        self._kernel_processing = []
        self._data_reader = []
        self._data_parser = []

    def add_plugins(self, plugins):
        for plugin in plugins:
            self._plugin_filter(plugin)

    def _plugin_filter(self, plugin):
        try:
            temp_object = plugin()
            plugin_type = temp_object.request_metadata("provides")

            if plugin_type == "data reader":
                self._data_reader.append(plugin)
            elif plugin_type == "data parser":
                self._data_parser.append(plugin)
            elif plugin_type == "minimization":
                self._minimization.append(plugin)
            elif plugin_type == "kernel processing":
                self._kernel_processing.append(plugin)

        except Exception as Error:
            self._logger.error(Error)

    def search_plugin(self, plugin_name, plugin_type):
        if plugin_type is "data reader":
            return self._plugin_name_search(
                plugin_name, self._data_reader
            )

        elif plugin_type is "data parser":
            return self._plugin_name_search(
                plugin_name, self._data_parser
            )

        elif plugin_type is "minimization":
            return self._plugin_name_search(
                plugin_name, self._minimization
            )

        elif plugin_type is "kernel processing":
            return self._plugin_name_search(
                plugin_name, self._kernel_processing
            )

    @staticmethod
    def _plugin_name_search(plugin_name, plugins):
        for plugin in plugins:
            if plugin["name"] == plugin_name:
                return plugin
        else:
            raise ImportError(
                "Failed to find plugin {0}".format(plugin_name)
            )

    @property
    def minimization(self):
        return self._minimization

    @property
    def kernel_processing(self):
        return self._kernel_processing

    @property
    def data_reader(self):
        return self._data_reader

    @property
    def data_parser(self):
        return self._data_parser


class MakeConfiguration(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        self._plugin_handler = plugin_loader.PluginLoading(
            option_templates.PluginsOptionsTemplate
        )

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

        storage = MetadataStorage()
        storage.add_plugins(plugins)

        selected_plugins = self._parse_plugins(main_plugin, storage)
        configuration = self._build_configuration(selected_plugins)

        fixed_config = self._correct_main_name(
            main_plugin, plugin_name, configuration, provided_options
        )

        self._write_config(fixed_config)

    def _write_config(self, configuration):
        string = """\
What would you like to name the configuration file?
[File Name?]: """

        if len(self._save_location):
            while True:
                value = input(string)

                if self._is_correct(value):
                    self._save_location = value
                    break

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
        if provided_options:
            for option in provided_options:
                configuration[main_name].pop(option)

        configuration[main_name] = \
            configuration[main_plugin.request_options("id")]

        configuration.pop(main_plugin.request_options("id"))

        return configuration

    def _build_configuration(self, plugin_list):
        """

        Args:
            plugin_list (list[option_templates.PluginsOptionsTemplate]):

        Returns:

        """
        configuration = {}
        for plugin in plugin_list:
            configuration[plugin.request_metadata("name")] = \
                plugin.request_options(self._level)

        return configuration

    def _parse_plugins(self, main_plugin, storage):
        """

        Args:
            main_plugin (option_templates.MainOptionsTemplate):
            storage:

        Returns:

        """
        plugins = []
        if main_plugin.requires("data parser"):
            plugins.append(self._process_plugins(
                "data parser", "Data Parsing", storage
            ))

        if main_plugin.requires("data reader"):
            plugins.append(self._process_plugins(
                "data reader", "Data Iterator", storage
            ))

        if main_plugin.requires("kernel processing"):
            plugins.append(self._process_plugins(
                "kernel processing", "Kernel Processor", storage
            ))

        if main_plugin.requires("minimization"):
            plugins.append(self._process_plugins(
                "minimization", "Minimizer", storage
            ))

        return plugins

    def _process_plugins(self, plugin_type, plugin_type_name, storage):

        if len(storage.data_parser) == 1:
            return storage.data_parser[0]
        else:
            name = self._ask_plugin(
                storage.data_parser, plugin_type_name
            )

            return storage.search_plugin(name, plugin_type)

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

        while True:
            value = input(string)

            corrected_value = fuzzywuzzy.process.extractOne(value, names)
            if corrected_value[1] > FUZZY_STRING_CONFIDENCE_LEVEL:
                if self._is_correct(corrected_value[0]):
                    return corrected_value[0]

    def _request_plugin(self):
        string = """
Would you like to use your own plugins? If YES then please enter the
location, if NO then just press ENTER.
[None]: """

        while True:
            answer = input(string)

            if len(answer) == 0:
                return False
            elif not os.path.isdir(answer):
                print("Error! '{0}' Doesn't Exist!".format(answer))
            elif self._is_correct(answer):
                return answer

    def _request_level(self):
        string = """\
How much control would you like to have over the configuration?
required
optional (default, recommended)
advanced

[optional]: """

        while True:
            answer = input(string)
            if len(answer) == 0:
                answer = "optional"
                return answer

            new_answer = fuzzywuzzy.process.extractOne(
                answer, ["required", "optional", "advanced"]
            )

            if new_answer[1] > FUZZY_STRING_CONFIDENCE_LEVEL:
                if self._is_correct(new_answer[0]):
                    self._level = new_answer[0]

    def _is_correct(self, answer):
        string = """\
It looks like you selected '{0}', is this correct?
[Y]es/No: """

        while True:
            is_correct = input(string.format(answer))

            value = fuzzywuzzy.process.extractOne(
                is_correct.lower(), ["yes", "no"]
            )

            if value[1] > FUZZY_STRING_CONFIDENCE_LEVEL:
                if value[0] == "yes":
                    return True
                else:
                    return False
