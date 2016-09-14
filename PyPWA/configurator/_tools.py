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

import PyPWA.libs
import PyPWA.shell
import fuzzywuzzy.process
import numpy
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
