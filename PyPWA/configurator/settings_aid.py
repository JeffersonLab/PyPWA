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
#TODO
"""

import logging

import fuzzywuzzy.process
import numpy

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


FUZZY_STRING_CONFIDENCE_LEVEL = 75  # percent from 0 to 100


# TODO: Separate logic types into different objects
# TODO: Make the Settings more SOLID
# TODO: Clean up the documentation some.
# TODO: Make more todo lists.


class BaseSettings(object):
    """
    Base Object for manipulating the settings dictionaries are loaded from
    the yaml and passed to each of the plugins and modules. Should help
    simplify the process of parsing arguments and even account for user
    error to a degree.
    """

    @staticmethod
    def _string_to_bool(string):
        """
        Converts a string to a bool with a level of certainty.

        Args:
            string (str): The string that needs to be converted into a
                bool.

        Returns:
            bool: If the conversion was successful.
            None: If the conversion fails.
        """
        value = fuzzywuzzy.process.extractOne(string, ["true", "false"])
        if value[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
            if value[0] == "true":
                return True
            elif value[0] == "false":
                return False
            else:
                return None
        else:
            return None

    @staticmethod
    def _return_options(string):
        """
        Extracts options from a single string for inline option parsing.

        Args:
            string (str): The string to be rendered by plugins that
                support it.

        Returns:
            list[str]: The extracted options, non-parsed.
        """
        options = []
        for possible_option in string.split(";"):
            if "=" in possible_option:
                options.append(possible_option)
        return options

    @staticmethod
    def _extract_options(supported_options, options):
        """
        Extracts the options from an non-parsed string.

        Args:
            supported_options (list[str]): The list of possible options
                that are supported.
            options (list[str]): The list of the non-parsed options.

        Returns:
            dict: The completely parsed options from the string.
                Option = Value
        """
        correct_options = {}
        for possible_option in options:
            option = possible_option.split("=")[0]
            the_value = option.split("=")[1]

            the_key = fuzzywuzzy.process.extractOne(
                option, supported_options
            )

            if the_key[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
                correct_options[the_key[0]] = the_value
        return correct_options

    @staticmethod
    def _correct_values(supported_values, value):
        """
        Corrects a single value to match what is expected.
        Args:
            supported_values (list[str]): The possible values.
            value (str): The parsed value.

        Returns:
            str: The corrected value.
        """
        possible_value = fuzzywuzzy.process.extractOne(
            value, supported_values
        )

        if possible_value[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
            return possible_value[0]
        else:
            return None

    def _dict_values(self, found_value, template_value):
        """
        Corrects the dictionary based off another dictionary.

        Args:
            found_value (string): The parsed dictionary with corrected
                keys.
            template_value (type): The template dictionary that contains
                all the possible options and values.

        Returns:
            dict: The corrected dictionary.
        """

        # Checks for types that are known, but could be any value
        if isinstance(template_value, type):
            if template_value == bool:
                return self._string_to_bool(found_value)
            elif template_value == str:
                return str(found_value)
            elif template_value == int:
                try:
                    return int(found_value)
                except ValueError:
                    return None
            elif template_value == numpy.float64:
                try:
                    return numpy.float64(found_value)
                except ValueError:
                    return None
            return None

        elif isinstance(template_value, list):
            return self._correct_values(template_value, found_value)
        else:
            return None


class CorrectSettings(BaseSettings):

    def __init__(self):
        """
        Corrects simple settings.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    def correct_dictionary(self, the_dictionary, template_dictionary):
        """
        Corrects the values and keys.

        Args:
            the_dictionary (dict): The parsed dictionary.
            template_dictionary (dict): The template dictionary.

        Returns:
            dict: The corrected dictionary.
        """
        corrected_dict = {}
        correct_keys = list(template_dictionary.keys())
        for key in the_dictionary:
            potential_key = fuzzywuzzy.process.extractOne(
                key, correct_keys
            )

            if potential_key[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:

                value = self._dict_values(
                    the_dictionary[key],
                    template_dictionary[potential_key]
                )

                if not isinstance(value, type(None)):
                    corrected_dict[potential_key] = value

# Accidental Mess