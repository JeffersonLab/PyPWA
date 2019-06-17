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
Intelligently loads user created configuration files
====================================================
This loads configuration files in YAML or JSON and attempts to correct any user
errors that might be in the configuration file before converting the values
into the correct data types.

Layout:
-------
- Data Types and globals: Custom data types used for configuration, static
    globals for the script
- Parse: Parses the configuration file and attempts to correct values if
    possible. Supports YAML and JSON
- Write: Returns a configuration file in YAML, or JSON if specified.

"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Union, Optional, List

import numpy as npy
import yaml

from PyPWA import AUTHOR, VERSION

"""fuzzywuzzy is an optional dependency
Fuzzywuzzy handles correcting string values when there is a known list
of potential values for that string. It isn't necessary for the program
to run, but does correct for potential user spelling errors in the
configuration file.

This is used to correct for options with a set number of expected string
values, and for correcting dictionary keys.
"""

try:
    _FUZZING = True  # This is broken in a really bad way
    import fuzzywuzzy.process

except ImportError:
    _FUZZING = False

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


"""
Data Types and Globals
"""

_OPTIONS = Dict[str, Any]
_TEMPLATE = Dict[str, Union[type, Dict[str, type], List[str]]]

# Controls the threshold for when a value is accepted or not
_FUZZY_STRING_CONFIDENCE_LEVEL = 75
_LOGGER = logging.getLogger(__name__)

if not _FUZZING:
    _LOGGER.debug("Fuzzing is not enabled, fuzzywuzzy not found.")

"""
Parse
"""


def parse(location: Path, template: Optional[_TEMPLATE] = None) -> _OPTIONS:
    # Easier to ask for forgiveness than to ask for permission
    with location.open() as stream:
        try:
            parsed = yaml.load(stream, Loader=yaml.FullLoader)
        except Exception as yaml_error:
            stream.seek(0)
            try:
                parsed = json.load(stream)
            except Exception as json_error:
                raise ValueError(
                    f"Failed to parse the configuration file!\n"
                    f"YAML Error: \n"
                    f"{yaml_error} \n\n"
                    f"JSON Error: \n"
                    f"{json_error}"
                )

    # If we're provided a template, we'll use it to correct the dictionary
    if isinstance(template, dict):
        parsed = _correct_keys(parsed, template)
        parsed = _correct_values(parsed, template)

    return parsed


def _correct_keys(parsed: _OPTIONS, template: _TEMPLATE) -> _OPTIONS:
    if _FUZZING:
        corrected = dict()
        correct_keys = list(template.keys())

        for key in parsed.keys():
            # Handle situations where the there are no provided keys
            try:
                fuzz = fuzzywuzzy.process.extractOne(key, correct_keys)
            except RuntimeError:
                fuzz = (0, 0)

            if fuzz[1] >= _FUZZY_STRING_CONFIDENCE_LEVEL:
                found = fuzz[0]
            else:
                _LOGGER.info(f"Failed to find: {key}. Fuzz results: {fuzz!r}")
                found = key

            if found in correct_keys and isinstance(template[found], dict):
                corrected[found] = _correct_keys(parsed[key], template[found])
            else:
                corrected[found] = parsed[key]

        return corrected
    else:
        return parsed


def _correct_values(parsed: _OPTIONS, template: _TEMPLATE) -> _OPTIONS:
    corrected = dict()

    for key in parsed.keys():
        # Skip keys that are not in the template
        if key not in template:
            corrected[key] = parsed[key]
            continue

        if isinstance(parsed[key], type(None)):
            corrected[key] = None

        elif template[key] == int:
            corrected[key] = int(parsed[key])

        elif template[key] == float:
            corrected[key] = npy.float64(parsed[key])

        elif template[key] == bool:
            corrected[key] = bool(parsed[key])

        # Some parsers might cast strings of numerical values to a numerical
        # type when we actually want the string
        elif template[key] == str:
            corrected[key] = str(parsed[key])

        # If the value is already a list, it wont wrap it in another list
        elif template[key] == list:
            corrected[key] = list(parsed[key])

        # Same as above
        elif template[key] == set:
            corrected[key] = set(parsed[key])

        # If a list of potential options are provided, this will correct the
        # value to be one of those provided options if possible
        elif isinstance(template[key], list):
            if _FUZZING:
                fuzz = fuzzywuzzy.process.extractOne(parsed[key], template[key])
                if fuzz[1] >= _FUZZY_STRING_CONFIDENCE_LEVEL:
                    corrected[key] = fuzz[0]
                else:
                    raise ValueError(
                        f"{parsed[key]!r} not found in {template[key]!r}! "
                        f"Fuzzing results: {fuzz}"
                    )
            else:
                corrected[key] = parsed[key]

        # Handle nested options
        elif isinstance(template[key], dict):
            corrected[key] = _correct_values(parsed[key], template[key])

        # Handle improperly configured configuration template
        else:
            raise ValueError(f"Unknown template type: {template[key]}")

    return corrected


"""
Write
"""


def write(filename: Union[Path, str], configuration: _OPTIONS):
    filename = Path(filename).absolute()

    with filename.open('w') as stream:
        if filename.suffix == ".json":
            stream.write(json.dumps(configuration, indent=4))
        else:
            stream.write(yaml.dump(configuration))
