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
Handles the input for WriteConfig
---------------------------------

- _Input - Handles differences between Python 2 and Python 3

- _IsCorrect - Asks if the provided question is correct.

- SimpleInputObject - Is the main loop for questions that need to be asked.
"""

import logging
import os
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


class _IsCorrect(object):

    __QUERY = "It looks like you selected '{0}', is this correct?\n" + \
             "[Y]es/No: "

    __input = _Input()
    __auto_correct_percentage = None
    __input_data = None
    __processed_answer = None

    def __init__(self, auto_correct_percentage=75):
        self.__auto_correct_percentage = auto_correct_percentage

    def ask(self, value):
        self.__question_loop(value)
        return self.__process_final_answer()

    def __question_loop(self, value):
        while True:
            self.__get_value(value)

            if self.__input_data == "":
                self.__set_answer("yes")
                break

            self.__fuzz_value()
            if self.__answer_is_valid():
                break

    def __get_value(self, value):
        input_data = self.__input.input(self.__QUERY.format(value))
        self.__input_data = input_data.lower()

    def __set_answer(self, value):
        self.__processed_answer = [value, 100]

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


class SimpleInputObject(object):

    __logger = logging.getLogger(__name__ + ".SimpleInputObject")
    __input = _Input
    __is_correct = _IsCorrect

    __auto_correction_percentage = None
    __users_input = None
    __processed_value = None

    def __init__(self, auto_correct_percentage=75):
        self.__auto_correction_percentage = auto_correct_percentage
        self.__input = _Input()
        self.__is_correct = _IsCorrect()

    def input(
            self, string, possible_answers=False,
            default_answer=False
    ):
        self.__question_loop(string, possible_answers, default_answer)
        self.__logger.info("Found answer: %s" % self.__processed_value[0])
        return self.__processed_value[0]

    def __question_loop(
            self, string, possible_answers=False,
            default_answer=False
    ):
        self.__logger.debug("Question: %s" % string)
        self.__logger.debug("Potential Answers: %s" % possible_answers)
        self.__logger.debug("Default Answer: %s" % default_answer)

        while True:
            self.__get_input(string)

            if self.__users_input is "":
                if default_answer:
                    self.__set_processed_value(default_answer)
                    self.__logger.info(
                        "Using default answer: %s" % default_answer
                    )
                    break
                continue

            else:
                if possible_answers:
                    self.__process_value(possible_answers)

                    if self.__answer_is_valid():
                        break
                else:
                    break

    def __get_input(self, string):
        self.__users_input = self.__input.input(string)

    def __set_processed_value(self, value):
        self.__processed_value = [value, 100]

    def __process_value(self, possible_answers):
        self.__processed_value = fuzzywuzzy.process.extractOne(
            self.__users_input, possible_answers
        )

    def __answer_is_valid(self):
        if self.__processed_value[1] > self.__auto_correction_percentage:
            if self.__processed_value[1] < 95:
                return self.__is_correct.ask(self.__processed_value[0])
            else:
                return True
        else:
            return False
