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

import os
import sys

import fuzzywuzzy.process

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _Input(object):

    _version = sys.version_info.major

    def input(self, string):
        if self._version == 2:
            return self._python_2(string)
        else:
            return self._python_new(string)

    @staticmethod
    def _python_2(string):
        return raw_input(string)

    @staticmethod
    def _python_new(string):
        return input(string)


class _IsCorrect(object):

    _QUERY = "It looks like you selected '{0}', is this correct?\n" + \
             "[Y]es/No: "

    _input = _Input
    _auto_correct_percentage = None
    _input_data = None
    _processed_answer = None

    def __init__(self, auto_correct_percentage=90):
        self._input = _Input()
        self._auto_correct_percentage = auto_correct_percentage

    def ask(self, value):
        self._question_loop(value)
        return self._process_final_answer()

    def _question_loop(self, value):
        while True:
            self._get_value(value)

            if self._is_blank():
                self._set_answer("yes")
                break

            self._fuzz_value()
            if self._answer_is_valid():
                break

    def _get_value(self, value):
        input_data = self._input.input(self._QUERY.format(value))
        self._input_data = input_data.lower()

    def _is_blank(self):
        if self._input_data == "":
            return True
        else:
            return False

    def _set_answer(self, value):
        self._processed_answer = [value, 100]

    def _fuzz_value(self):
        choices = ["yes", "no"]

        self._processed_answer = fuzzywuzzy.process.extractOne(
            self._input_data, choices
        )

    def _answer_is_valid(self):
        if self._processed_answer[1] > self._auto_correct_percentage:
            return True
        else:
            return False

    def _process_final_answer(self):
        if self._processed_answer[0] == "yes":
            return True
        elif self._processed_answer[0] == "no":
            return False


class SimpleInputObject(object):

    _input = _Input
    _is_correct = _IsCorrect

    _auto_correction_percentage = None
    _users_input = None
    _processed_value = None

    def __init__(self, auto_correct_percentage=75):
        self._auto_correction_percentage = auto_correct_percentage
        self._input = _Input()
        self._is_correct = _IsCorrect()

    def input(
            self, string, possible_answers=False,
            default_answer=False, is_dir=False
    ):
        self._question_loop(string, possible_answers, default_answer, is_dir)
        return self._processed_value[0]

    def _question_loop(
            self, string, possible_answers=False,
            default_answer=False, is_dir=False
    ):

        while True:
            self._get_input(string)

            if self._answer_is_blank():
                if default_answer:
                    self._set_processed_value(default_answer)
                    break
                continue

            else:
                if possible_answers:
                    self._process_value(possible_answers)

                    if self._answer_is_valid():
                        continue
                if is_dir:
                    if not self._answer_is_directory():
                        continue
                if self._answer_is_correct():
                    break

    def _get_input(self, string):
        self._users_input = self._input.input(string)

    def _answer_is_blank(self):
        if self._users_input is "":
            return True
        else:
            return False

    def _set_processed_value(self, value):
        self._processed_value = [value, 100]

    def _process_value(self, possible_answers):
        self._processed_value = fuzzywuzzy.process.extractOne(
            self._users_input, possible_answers
        )

    def _answer_is_valid(self):
        if self._processed_value[1] > self._auto_correction_percentage:
            return True
        else:
            return False

    def _answer_is_directory(self):
        if os.path.isdir(self._processed_value[0]):
            return True
        else:
            return False

    def _answer_is_correct(self):
        if self._is_correct.ask(self._processed_value[0]):
            return True
        else:
            return False