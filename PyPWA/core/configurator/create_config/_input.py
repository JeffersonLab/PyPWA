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

    __version = sys.version_info.major

    def input(self, string):
        if self.__version == 2:
            return self.__python_2(string)
        else:
            return self.__python_new(string)

    @staticmethod
    def __python_2(string):
        return raw_input(string)

    @staticmethod
    def __python_new(string):
        return input(string)


class _IsCorrect(object):

    __QUERY = "It looks like you selected '{0}', is this correct?\n" + \
             "[Y]es/No: "

    __input = _Input
    __auto_correct_percentage = None
    __input_data = None
    __processed_answer = None

    def __init__(self, auto_correct_percentage=90):
        self.__input = _Input()
        self.__auto_correct_percentage = auto_correct_percentage

    def ask(self, value):
        self.__question_loop(value)
        return self.__process_final_answer()

    def __question_loop(self, value):
        while True:
            self.__get_value(value)

            if self._input_data == "":
                self.__set_answer("yes")
                break

            self.__fuzz_value()
            if self.__answer_is_valid():
                break

    def __get_value(self, value):
        input_data = self.__input.input(self.__QUERY.format(value))
        self._input_data = input_data.lower()

    def __set_answer(self, value):
        self._processed_answer = [value, 100]

    def __fuzz_value(self):
        choices = ["yes", "no"]

        self._processed_answer = fuzzywuzzy.process.extractOne(
            self._input_data, choices
        )

    def __answer_is_valid(self):
        if self._processed_answer[1] > self.__auto_correct_percentage:
            return True
        else:
            return False

    def __process_final_answer(self):
        if self._processed_answer[0] == "yes":
            return True
        elif self._processed_answer[0] == "no":
            return False


class SimpleInputObject(object):

    __input = _Input
    __is_correct = _IsCorrect

    __auto_correction_percentage = None
    __users_input = None
    __processed_value = None

    def __init__(self, auto_correct_percentage=75):
        self._auto_correction_percentage = auto_correct_percentage
        self._input = _Input()
        self._is_correct = _IsCorrect()

    def input(
            self, string, possible_answers=False,
            default_answer=False, is_dir=False
    ):
        self.__question_loop(string, possible_answers, default_answer, is_dir)
        return self._processed_value[0]

    def __question_loop(
            self, string, possible_answers=False,
            default_answer=False, is_dir=False
    ):

        while True:
            self.__get_input(string)

            if self.__users_input is "":
                if default_answer:
                    self.__set_processed_value(default_answer)
                    break
                continue

            else:
                if possible_answers:
                    self.__process_value(possible_answers)

                    if self.__answer_is_valid():
                        continue
                if is_dir:
                    if not os.path.isdir(self._processed_value[0]):
                        continue
                if self._is_correct.ask(self._processed_value[0]):
                    break

    def __get_input(self, string):
        self._users_input = self._input.input(string)

    def __set_processed_value(self, value):
        self._processed_value = [value, 100]

    def __process_value(self, possible_answers):
        self._processed_value = fuzzywuzzy.process.extractOne(
            self._users_input, possible_answers
        )

    def __answer_is_valid(self):
        if self._processed_value[1] > self._auto_correction_percentage:
            return True
        else:
            return False
