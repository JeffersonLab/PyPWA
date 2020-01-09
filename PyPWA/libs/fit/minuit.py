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

from PyPWA import info as _info
from typing import Any as _Any, Dict as _Dict, List as _List
import iminuit as _iminuit
from . import likelihoods as _likelihoods

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class Translator(_likelihoods.TranslatorInterface):

    def __init__(self, parameters: _List[str]):
        self.__parameters = parameters

    def __call__(self, *args: _List[float]) -> _Dict[str, _List[float]]:
        parameters_with_values = {}
        for parameter, arg in zip(self.__parameters, args[0][0]):
            parameters_with_values[parameter] = arg

        return parameters_with_values


def minimize(
        parameters: _Dict[str, _Any], settings: _Dict[str, _Any],
        likelihood: _likelihoods.ChiSquared, set_up: int, strategy=1,
        num_of_calls=1000, end_process=True
):
    settings["forced_parameters"] = parameters
    settings["errordef"] = set_up
    optimizer = _iminuit.Minuit(likelihood, **settings)

    optimizer.set_strategy(strategy)
    optimizer.set_up(set_up)
    optimizer.migrad(num_of_calls)

    if end_process:
        likelihood.stop()
    return optimizer
