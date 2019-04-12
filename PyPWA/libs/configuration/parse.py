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
"""

import yaml
import json

try:
    import fuzzywuzzy.process
    FUZZING = True
except ImportError:
    FUZZING = False


from typing import Any, Dict, List, Union, Tuple

from PyPWA import AUTHOR, VERSION, Path

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


_FUZZY_STRING_CONFIDENCE_LEVEL = 75


def correct_user_configuration(conf_filename, template_conf, default_conf):
    # type: (Path, Dict[str, Any], Dict[str, Any]) -> Dict[str, Any]
    user_conf = _ParseConf.parse(conf_filename)
    if FUZZING:
        key_correct = _CorrectKeys.correct_keys(user_conf, template_conf)
        value_correct = _CorrectValues.correct_all(key_correct, template_conf)
        return _add_defaults(value_correct, default_conf)
    else:
        return user_conf


class _ParseConf(object):

    @classmethod
    def parse(cls, conf_filename):
        # type: (Path) -> Dict[str, Any]
        yaml_attempt = cls.__load_yaml(conf_filename)
        if yaml_attempt[0]:
            return yaml_attempt[1]

        json_attempt = cls.__load_json(conf_filename)
        if json_attempt[0]:
            return json_attempt[1]

        raise RuntimeError(yaml_attempt[1], json_attempt[1])

    @staticmethod
    def __load_yaml(conf_filename):
        # type: (Path) -> Tuple[bool, Union[Dict[str, Any], Exception]]
        try:
            with conf_filename.open() as stream:
                return True, yaml.load(stream)
        except Exception as Error:
            return False, Error
    @staticmethod
    def __load_json(conf_filename):
        # type: (Path) -> Tuple[bool, Union[Dict[str, Any], Exception]]
        try:
            with conf_filename.open() as stream:
                return True, json.load(stream)
        except Exception as Error:
            return False, Error


class _CorrectKeys(object):

    @classmethod
    def correct_keys(cls, dictionary, template):
        # type: (Dict[str, Any], Dict[str, Any]) -> Dict[str, Any]
        corrected_keys = {}
        for initial_key in dictionary.keys():
            fuzzed = cls.__get_potential_key(initial_key, template)
            result = fuzzed if fuzzed else initial_key
            corrected_keys[result] = dictionary[initial_key]

            if isinstance(template[result], dict):
                corrected_keys[result] = cls.correct_keys(
                    dictionary[initial_key], template[result]
                )
        return corrected_keys

    @staticmethod
    def __get_potential_key(key, template):
        # type: (str, Dict[str, Any]) -> str
        found_key = fuzzywuzzy.process.extractOne(key, list(template.keys()))
        if found_key[1] >= _FUZZY_STRING_CONFIDENCE_LEVEL:
            return found_key[0]


class _CorrectValues(object):

    @classmethod
    def correct_all(cls, user_configuration, provided_template):
        # type: (Dict[str, Any], Dict[str, Any]) -> Dict[str, Any]
        corrected = {}
        for key in user_configuration.keys():
            template = provided_template[key]
            current = user_configuration[key]

            if isinstance(current, type(None)):
                corrected[key] = None
            elif template == int:
                corrected[key] = int(current)
            elif template == float:
                corrected[key] = float(current)
            elif template == bool:
                corrected[key] = bool(int(current))
            elif template == str:
                corrected[key] = str(current)
            elif template == list:
                corrected[key] = list(current)
            elif template == set:
                corrected[key] = set(current)
            elif template == Path:
                corrected[key] = Path(current)
            elif isinstance(template, list):
                corrected[key] = cls.__from_list(current, template)
            elif isinstance(template, dict):
                corrected[key] = cls.correct_all(current, template)
            else:
                corrected[key] = current
        return corrected

    @staticmethod
    def __from_list(string, value_list):
        # type: (str, List[str]) -> str
        value = fuzzywuzzy.process.extractOne(string, value_list)
        if value[1] >= _FUZZY_STRING_CONFIDENCE_LEVEL:
            return value[0]
        raise ValueError(
            "Can't find a value for {0} from {1}".format(string, value_list)
        )

    @staticmethod
    def __boolean(value):
        # type: (Union[int, str, bool]) -> bool
        try:
            return True if int(value) else False
        except ValueError:
            pass

        fuzzed = fuzzywuzzy.process.extractOne(value, ["true", "false"])
        if fuzzed[1] >= _FUZZY_STRING_CONFIDENCE_LEVEL:
            return True if fuzzed[0] == "true" else False
        raise ValueError("Can't translate {0} to boolean!".format(value))


def _add_defaults(user_conf, defaults):
    # type: (Dict[str, Any], Dict[str, Any]) -> Dict[str, Any]
    full_conf = {}
    for key in defaults.keys():
        if isinstance(defaults[key], dict) and key in list(user_conf.keys()):
            full_conf[key] = _add_defaults(user_conf[key], defaults[key])
        elif key in list(user_conf.keys()):
            full_conf[key] = user_conf[key]
        else:
            full_conf[key] = defaults[key]
    return full_conf
