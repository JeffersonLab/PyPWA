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
Handles all real input for Create Config
----------------------------------------

- _Input - Handles differences between Python 2 and 3

- _IsCorrectLoop - A simple loop that asks the user if about their input
  is fuzzing wasn't good enough.
  
- QuestionLoop - The main question loop, handles all input.
"""

import logging
import sys

import fuzzywuzzy.process

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
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


class _IsCorrectLoop(object):

    __logger = logging.getLogger(__name__ + "._IsCorrectLoop")
    __input = _Input()
    __auto_correct_percentage = 90
    __input_data = None
    __processed_answer = None

    def ask(self, value):
        self.__question_loop(value)
        return self.__process_final_answer()

    def __question_loop(self, value):
        while True:
            self.__get_answer(value)

            if self.__input_data == "":
                self.__assume_answer_is_correct()
                break

            self.__fuzz_value()
            if self.__answer_is_valid():
                break

    def __get_answer(self, value):
        input_data = self.__input.input(
            "It looks like you selected '%s', is this correct?\n"
            "[Y]es/No: " % value
        )
        self.__input_data = input_data.lower()

    def __assume_answer_is_correct(self):
        self.__processed_answer = ["yes", 100]

    def __fuzz_value(self):
        choices = ["yes", "no"]

        self.__processed_answer = fuzzywuzzy.process.extractOne(
            self.__input_data, choices
        )

    def __answer_is_valid(self):
        if self.__processed_answer[1] > self.__auto_correct_percentage:
            return True
        else:
            return False

    def __process_final_answer(self):
        if self.__processed_answer[0] == "yes":
            return True
        elif self.__processed_answer[0] == "no":
            return False


class QuestionLoop(object):

    __logger = logging.getLogger(__name__ + ".QuestionLoop")
    __input = _Input()
    __is_correct = _IsCorrectLoop()

    __users_input = None
    __processed_value = None

    _auto_correction_percentage = 75
    _question = None
    _possible_answers = False
    _default_answer = False

    def _question_loop(self):
        self.__log_initial_data()

        while True:
            self.__get_input(self._question)

            if self.__users_input is "":
                if self._default_answer:
                    self.__set_processed_value_to_default_answer()
                    break
                continue

            else:
                if self._possible_answers:
                    self.__process_input_using_known_values()

                    if self.__answer_is_valid():
                        break
                else:
                    self.__set_processed_value_to_user_input()
                    break

    def __log_initial_data(self):
        self.__logger.debug("Question: %s" % self._question)

        if self._possible_answers:
            self.__logger.debug(
                "Potential Answers: %s" % self._possible_answers
            )
        else:
            self.__logger.debug("No potential answers provided")

        if self._default_answer:
            self.__logger.debug("Default Answer: %s" % self._default_answer)
        else:
            self.__logger.debug("No default answer set.")

    def __get_input(self, string):
        self.__users_input = self.__input.input(string)

    def __set_processed_value_to_default_answer(self):
        self.__processed_value = [self._default_answer, 100]
        self.__logger.info("Using default answer: %s" % self._default_answer)

    def __process_input_using_known_values(self):
        self.__processed_value = fuzzywuzzy.process.extractOne(
            self.__users_input, self._possible_answers
        )

    def __answer_is_valid(self):
        if self.__processed_value[1] > self._auto_correction_percentage:
            if self.__processed_value[1] < 95:
                return self.__is_correct.ask(self.__processed_value[0])
            else:
                return True
        else:
            return False

    def __set_processed_value_to_user_input(self):
        self.__processed_value = [self.__users_input, 100]
        self.__logger.info("Setting answer to %s" % self.__users_input)

    @property
    def _answer(self):
        return self.__processed_value[0]
