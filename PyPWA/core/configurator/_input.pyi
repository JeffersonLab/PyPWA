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

import typing

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _Input(object):

    _version = ...  # type: int

    def input(self, string: str) -> str: ...

    @staticmethod
    def _python_2(string: str) -> str: ...

    @staticmethod
    def _python_new(string: str) -> str: ...


class _IsCorrect(object):

    _QUERY = "It looks like you selected '{0}', is this correct?\n" + \
             "[Y]es/No: "

    _input = ...  # type: _Input
    _auto_correct_percentage = ...  # type: float
    _input_data = ...  # type: str
    _processed_answer = ...  # type: typing.Tuple[str, float]

    def __init__(self, auto_correct_percentage: typing.Optional[float]): ...

    def ask(self, value: str) -> bool: ...

    def _question_loop(self, value: str): ...

    def _get_value(self, value: str): ...

    def _is_blank(self) -> bool: ...

    def _set_answer(self, value: str): ...

    def _fuzz_value(self): ...

    def _answer_is_valid(self) -> bool: ...

    def _process_final_answer(self) -> bool: ...


class SimpleInputObject(object):

    _input = ...  # type: _Input
    _is_correct = ...  # type: _IsCorrect

    _auto_correction_percentage = ...  # type: float
    _users_input = ...  # type: str
    _processed_value = ...  # type: typing.Tuple[str, float]

    def __init__(self, auto_correct_percentage: typing.Optional[float]): ...

    def input(self, string: str, possible_answers: typing.Any,
              default_answer: typing.Any, is_dir: typing.Any
    ) -> str: ...

    def _question_loop(
            self, string: str, possible_answers: typing.Any,
            default_answer: typing.Any, is_dir: typing.Any
    ): ...

    def _get_input(self, string: str): ...

    def _answer_is_blank(self) -> bool: ...

    def _set_processed_value(self, value: str): ...

    def _process_value(self, possible_answers: typing.List[str]): ...

    def _answer_is_valid(self) -> bool: ...

    def _answer_is_directory(self) -> bool: ...

    def _answer_is_correct(self) -> bool: ...
