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

from typing import Any, Callable as Call, Dict, List, Union

import iminuit as _iminuit
import numpy as np

from PyPWA import info
from . import likelihoods

__credits__ = ["Mark Jones"]
__author__ = info.AUTHOR
__version__ = info.VERSION


class _Translator:

    def __init__(
            self,
            parameters: Union[List[str], None],
            function_call: Call[[Any], float]
    ):
        self.__parameters = parameters
        self.__function = function_call

        if self.__parameters is None:
            self.__call = self.__passthrough
        else:
            self.__call = self.__with_parameters

    def __call__(self, *args):
        return self.__call(*args)

    def __passthrough(self, array) -> float:
        return self.__function(array)

    def __with_parameters(self, *args: List[float]) -> float:
        parameters_with_values = {}
        for parameter, arg in zip(self.__parameters, args):
            parameters_with_values[parameter] = arg

        return self.__function(parameters_with_values)


def minuit(
        settings: Union[Dict[str, Any], np.ndarray],
        likelihood: likelihoods.ChiSquared
):
    """Optimization using iminuit

    Parameters
    ----------
    settings : Dict[str, Any]
        The settings to be passed to iminuit. Look into the documentation
        for iminuit for specifics
    likelihood : Likelihood object from likelihoods or single function

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
    if isinstance(settings, np.ndarray):
        name = None
    elif "name" not in settings:
        name = list(settings.keys())
    else:
        name = settings["name"]

    translator = _Translator(name, likelihood)

    if name is None:
        optimizer = _iminuit.Minuit(translator, settings)
    else:
        optimizer = _iminuit.Minuit(translator, name=name, **settings)

    # Set error for Likelihood, Migrad defaults to ChiSquared
    if hasattr(likelihood, "TYPE"):
        if likelihood.TYPE == likelihoods.LikelihoodType.LIKELIHOOD:
            optimizer.errordef = _iminuit.Minuit.LIKELIHOOD
        elif likelihood.TYPE == likelihoods.LikelihoodType.CHI_SQUARED:
            optimizer.errordef = _iminuit.Minuit.LEAST_SQUARES

    return optimizer
