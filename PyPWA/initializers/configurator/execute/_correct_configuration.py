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
Attempts to correct the received settings if possible.
------------------------------------------------------

- _CorrectKeys - Iterates through all keys and sub-dictionaries of a 
  dictionary and then tries to correct the key names if possible.
  
- _CorrectValues - Attempts to correct the value of each key inside the 
  dictionary if possible.
  
- SettingsAid - Takes the template dictionary and the received dictionary 
  and attempts to correct all of the values.
"""

import logging
from typing import Any, Dict, List, Union, Tuple

import fuzzywuzzy.process
import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.initializers.configurator.execute import _storage_data

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


FUZZY_STRING_CONFIDENCE_LEVEL = 75


class _CorrectKeys(object):

    __LOGGER = logging.getLogger(__name__ + "._CorrectKeys")

    def __init__(self, template, depth=0):
        # type: (Dict[str, Any], int) -> None
        self.__depth = depth
        self.__template = template
        self.__LOGGER.debug("Received template: %s" % template)
        self.__initial_settings = None  # type: Dict[str, Any]
        self.__corrected_keys = None  # type: Dict[str, Any]
        self.__set_keys()

    def __set_keys(self):
        self.__keys = list(self.__template.keys())

    def correct_keys(self, dictionary):
        # type: (Dict[str, Any]) -> Dict[str, Any]
        self.__empty_corrected()
        self.__set_initial_settings(dictionary)
        self.__loop_over_keys()
        return self.__corrected_keys

    def __empty_corrected(self):
        self.__corrected_keys = {}

    def __set_initial_settings(self, settings):
        # type: (Dict[str, Any]) -> None
        self.__initial_settings = settings

    def __loop_over_keys(self):
        for key in self.__initial_settings.keys():
            found = self.__get_potential_key(key)
            if found:
                self.__set_corrected_key(found, key)
            else:
                self.__handle_key_error(key)
            self.__check_for_dictionary(found)

    def __get_potential_key(self, key):
        # type: (str) -> str
        found_key = self.__fuzz_key(key)
        if found_key[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
            return found_key[0]

    def __fuzz_key(self, key):
        # type: (str) -> Tuple(str, int)
        found_key = fuzzywuzzy.process.extractOne(key, self.__keys)
        return found_key

    def __set_corrected_key(self, found, key):
        # type: (str, str) -> None
        self.__corrected_keys[found] = self.__initial_settings[key]

    def __check_for_dictionary(self, found):
        # type: (str) -> None
        if isinstance(self.__template[found], dict):
            self.__LOGGER.debug(
                "Correcting internal dictionary: %s" % self.__template[found]
            )
            self.__correct_nested_dictionary(found)

    def __correct_nested_dictionary(self, found):
        # type: (str) -> None
        correction = _CorrectKeys(self.__template[found], self.__depth + 1)
        corrected = correction.correct_keys(self.__corrected_keys[found])
        self.__corrected_keys[found] = corrected

    def __handle_key_error(self, key):
        # type: (str) -> None
        if self.__depth:
            raise ValueError(
                "Root level key error! Unknown Plugin '%s'!" % key
            )
        else:
            self.__LOGGER.warning(
                "Unknown key '%s', value is being removed!" % key
            )


class _CorrectValues(object):

    __LOGGER = logging.getLogger(__name__ + "._CorrectValues")
    __FAILED = "failed to find"

    def correct_all(self, dictionary, template_dictionary):
        # type: (Dict[str, Any], Dict[str, Any]) -> Dict[str, Any]
        corrected_dictionary = {}
        for key in dictionary.keys():
            template_value = template_dictionary[key]
            current_value = dictionary[key]

            if isinstance(current_value, type(None)):
                corrected_dictionary[key] = None

            elif template_value == int:
                corrected_dictionary[key] = self.__correct_integers(
                    current_value
                )

            elif template_value == float:
                corrected_dictionary[key] = self.__correct_floats(
                    current_value
                )

            elif template_value == bool:
                corrected_dictionary[key] = self.__correct_boolean_values(
                    current_value
                )

            elif template_value == str:
                corrected_dictionary[key] = str(current_value)

            elif template_value == list:
                corrected_dictionary[key] = list(current_value)

            elif template_value == set:
                corrected_dictionary[key] = set(current_value)

            elif isinstance(template_value, list):
                corrected_dictionary[key] = self.__correct_from_list(
                    current_value, template_value
                )

            elif isinstance(template_value, dict):
                corrected_dictionary[key] = self.correct_all(
                    current_value, template_value
                )

            else:
                self.__LOGGER.debug(
                    "Key '%s' is not correctable by settings aid because "
                    "its expected value is not known." % key
                )

                corrected_dictionary[key] = current_value

        return corrected_dictionary

    def __correct_from_list(self, string, value_list):
        # type: (Union[str, Dict], List[Union[str, Dict]]) -> Union[str, List]
        if isinstance(value_list[0], str):
            value = fuzzywuzzy.process.extractOne(string, value_list)
            if value[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
                return value[0]
            else:
                return self.__FAILED
        else:
            return [self.correct_all(pv, value_list[0]) for pv in string]

    def __correct_boolean_values(self, value):
        # type: (Any) -> Union[bool, str]
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
                return self.__FAILED
        else:
            return self.__FAILED

    def __correct_integers(self, value):
        # type: (Any) -> Union[int, str]
        try:
            return int(value)
        except ValueError:
            return self.__FAILED

    def __correct_floats(self, value):
        # type: (Any) -> Union[numpy.float64, str]
        try:
            return numpy.float64(value)
        except ValueError:
            return self.__FAILED


class SettingsAid(object):

    __LOGGER = logging.getLogger(__name__ + ".SettingsAid")

    def __init__(self):
        self.__template = _storage_data.Templates()
        self.__key_corrector = _CorrectKeys(self.__template.get_templates())
        self.__correct_values = _CorrectValues()
        self.__settings = None

    def correct_settings(self, value):
        # type: (Dict[str, Any]) -> Dict[str, Any]
        self.__set_settings(value)
        self.__correct_keys()
        self.__correct_all()
        return self.__settings

    def __set_settings(self, values):
        # type: (Dict[str, Any]) -> None
        self.__settings = values

    def __correct_keys(self):
        self.__settings = self.__key_corrector.correct_keys(self.__settings)

    def __correct_all(self):
        self.__settings = self.__correct_values.correct_all(
            self.__settings, self.__template.get_templates()
        )
