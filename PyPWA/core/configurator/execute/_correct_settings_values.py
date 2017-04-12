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

import fuzzywuzzy.process
import numpy

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


FUZZY_STRING_CONFIDENCE_LEVEL = 75


class _CorrectKeys(object):

    __logger = logging.getLogger(__name__ + "._CorrectKeys")

    __TEMPLATE = None
    __KEYS = None
    __initial_settings = None
    __corrected_keys = None

    def __init__(self, template):
        self.__logger.addHandler(logging.NullHandler())
        self.__TEMPLATE = template  # type: dict
        self.__logger.debug("Received template: %s" % template)
        self.__set_keys()

    def __set_keys(self):
        self.__KEYS = list(self.__TEMPLATE.keys())

    def correct_keys(self, dictionary):
        self.__empty_corrected()
        self.__set_initial_settings(dictionary)
        self.__loop_over_keys()
        return self.__corrected_keys

    def __empty_corrected(self):
        self.__corrected_keys = {}

    def __set_initial_settings(self, settings):
        self.__initial_settings = settings

    def __loop_over_keys(self):
        for key in self.__initial_settings.keys():
            found = self.__get_potential_key(key)
            if found:
                self.__set_corrected_key(found, key)
            else:
                self.__log_key_error(key)
            self.__check_for_dictionary(found)

    def __get_potential_key(self, key):
        found_key = self.__fuzz_key(key)
        if found_key[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
            return found_key[0]

    def __fuzz_key(self, key):
        found_key = fuzzywuzzy.process.extractOne(key, self.__KEYS)
        return found_key

    def __set_corrected_key(self, found, key):
        self.__corrected_keys[found] = self.__initial_settings[key]

    def __check_for_dictionary(self, found):
        if isinstance(self.__TEMPLATE[found], dict):
            self.__logger.debug(
                "Correcting internal dictionary: %s" % self.__TEMPLATE[found]
            )
            self.__correct_nested_dictionary(found)

    def __correct_nested_dictionary(self, found):
        correction = _CorrectKeys(self.__TEMPLATE[found])
        corrected = correction.correct_keys(self.__corrected_keys[found])
        self.__corrected_keys[found] = corrected

    def __log_key_error(self, key):
        self.__logger.warning(
            "Unknown key %s, value is being removed!" % key
        )


class _CorrectValues(object):

    __logger = logging.getLogger(__name__ + "._CorrectValues")
    __FAILED = "failed to find"

    def correct_all(self, dictionary, template_dictionary):
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
                self.__logger.debug(
                    "Key {0} is not correctable by settings "
                    "aid.".format(key)
                )

                corrected_dictionary[key] = current_value

        return corrected_dictionary

    def __correct_from_list(self, string, value_list):
        value = fuzzywuzzy.process.extractOne(string, value_list)

        if value[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
            return value[0]
        else:
            return self.__FAILED

    def __correct_boolean_values(self, value):
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
        try:
            return int(value)
        except ValueError:
            return self.__FAILED

    def __correct_floats(self, value):
        try:
            return numpy.float64(value)
        except ValueError:
            return self.__FAILED


class SettingsAid(object):

    __logger = logging.getLogger(__name__ + ".SettingsAid")
    __correct_values = _CorrectValues()
    __key_corrector = None  # type: _CorrectKeys

    __TEMPLATE = None
    __settings = None

    def __init__(self, template):
        self.__logger.addHandler(logging.NullHandler())
        self.__TEMPLATE = template
        self.__key_corrector = _CorrectKeys(template)

    def correct_settings(self, value):
        self.__set_settings(value)
        self.__correct_keys()
        self.__correct_all()
        return self.__settings

    def __set_settings(self, values):
        self.__settings = values

    def __correct_keys(self):
        self.__settings = self.__key_corrector.correct_keys(self.__settings)

    def __correct_all(self):
        self.__settings = self.__correct_values.correct_all(
            self.__settings, self.__TEMPLATE
        )
