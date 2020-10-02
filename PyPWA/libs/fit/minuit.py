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

from typing import Any as _Any, Callable as _Call, Dict as _Dict, List as _List

import iminuit as _iminuit

from PyPWA import info as _info
from . import likelihoods as _likelihoods

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class _Translator:

    def __init__(
            self, parameters: _List[str], function_call: _Call[[_Any], float]
    ):
        self.__parameters = parameters
        self.__function = function_call

    def __call__(self, *args: _List[float]) -> float:
        parameters_with_values = {}
        for parameter, arg in zip(self.__parameters, args):
            parameters_with_values[parameter] = arg

        return self.__function(parameters_with_values)


def minuit(
        parameters: _List[str], settings: _Dict[str, _Any],
        likelihood: _likelihoods.ChiSquared, set_up: int, strategy=1,
        num_of_calls=1000
):
    """Optimization using iminuit

    Parameters
    ----------
    parameters : List[str]
        The names of the parameters for iminuit to use
    settings : Dict[str, Any]
        The settings to be passed to iminuit. Look into the documentation
        for iminuit for specifics
    likelihood : Likelihood object from likelihoods or single function
    set_up : float
        Set to 1 for log-likelihoods, or .5 for Chi-Squared
    strategy : int
        Fitting strategy. Defaults to 1. 0 is slowest, 2 is fastest/
    num_of_calls : int
        A suggested max number of calls to minuit. This may or may not
        be respected.

    Returns
    -------
    iminuit.Minuit
        The minuit object after the fit has been completed.

    Note
    ----
        See `Iminuit's documentation <https://iminuit.readthedocs.io/>`_
        for more imformation, as it should explain the various options
        that can be passed to iminuit, and how to use the resulting object
        after a fit has been completed.
    """
    settings["forced_parameters"] = parameters
    settings["errordef"] = set_up
    translator = _Translator(parameters, likelihood)
    optimizer = _iminuit.Minuit(translator, **settings)

    optimizer.strategy = strategy
    optimizer.errordef = set_up
    optimizer.migrad(num_of_calls)

    return optimizer
