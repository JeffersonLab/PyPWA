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

"""

import sys


try:
    import fuzzywuzzy.process
    FUZZING = True
except ImportError:
    FUZZING = False


from typing import List, Tuple, Optional as Opt
from PyPWA.libs.components.configuration import create

from PyPWA import AUTHOR, VERSION, Path

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


def ask_for_save_location():
    question = _question_loop("""
What would you like to name the configuration file?
File Name: """)
    return Path(question)


def ask_which_component(component_type, components, default=None):
    question = "What would you like to use for {0}?\n{1}".format(
        component_type, "/n".join(components)
    )

    if len(components) > 1:
        return _question_loop(question, components, default)
    else:
        return components[0]


def ask_for_configuration_difficulty():
    return {
        "Required": create.Verbosity.REQUIRED,
        "Optional": create.Verbosity.OPTIONAL,
        "Advanced": create.Verbosity.ADVANCED
    }[
        _question_loop(
            """
            How verbose would you like your configuration file? 
            Required
            Optional (default, recommended)
            Advanced
        
            [Optional]: """, ["Required", "Optional", "Advanced"], "Optional"
        )
    ]


def _question_loop(question, choices=None, default=None, fuzz_percentage=75):
    # type: (str, Opt[List[str]], Opt[str], Opt[int]) -> str
    while True:
        answer = _input(question)
        if answer is "" and default:
            return default
        else:
            if choices:
                fuzzed = fuzzywuzzy.process.extractOne(answer, choices)
                if _answer_is_valid(fuzzed, fuzz_percentage):
                    return fuzzed[0]
            else:
                return answer


def _input(string):
    if sys.version_info.major == 2:
        return raw_input(string)
    else:
        return input(string)


def _answer_is_valid(fuzzed, fuzzed_percentage):
    # type: (Tuple[str, int], int) -> bool
    if 90 > fuzzed[1] > fuzzed_percentage:
        return _verify_with_user(fuzzed[0])
    elif fuzzed[1] >= 90:
        return True
    else:
        return False


def _verify_with_user(value, fuzz_percentage = 90):
    # type: (str, Opt[int]) -> bool
    while True:
        user_answer = _input(
            "It looks like you selected '%s', is this correct?\n"
            "[Y]es/No: " % value
        ).lower()

        if user_answer == "":
            return True

        fuzzed = fuzzywuzzy.process.extractOne(user_answer, ['yes', 'no'])
        if fuzzed[1] > fuzz_percentage:
            return True if fuzzed[0] == 'yes' else False
