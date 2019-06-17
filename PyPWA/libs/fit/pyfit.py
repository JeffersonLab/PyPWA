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
PyFit, a flexible python fitting utility.
-----------------------------------------
- _LikelihoodPackager - a simple object that searches the 'likelihoods'
  package for the user's selected likelihood.
- Fitting - defines the actual main logic for the program.
"""

import logging
from dataclasses import dataclass
from typing import Any, Callable, Dict, List

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.libs import plugin_loader
from PyPWA.libs.components.fit import _process_interface, minuit, fit_plugin
from PyPWA.plugins import likelihoods

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


@dataclass
class FitData:
    # This is all the different data values that PyFit supports.
    data: Dict[str, numpy.ndarray]
    monte_carlo: Dict[str, numpy.ndarray]
    quality_factor: Dict[str, numpy.ndarray]
    binned: Dict[str, numpy.ndarray]
    events_errors: Dict[str, numpy.ndarray]
    expected_values: Dict[str, numpy.ndarray]
    generated_length: numpy.float64


@dataclass
class CallPackage:
    setup: Callable[[], None]
    run: Callable[[Any], float]


class LikelihoodFetch(object):

    __LOGGER = logging.getLogger(__name__ + ".PluginSearch")

    def __init__(self):
        self.__found_plugins = plugin_loader.fetch_plugins(
            likelihoods, "Likelihood"
        )

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

    def get_likelihood(self, name) -> fit_plugin.Setup:
        for likelihood in self.__found_plugins:
            if likelihood.name == name:
                return likelihood
        raise ValueError("Unknown likelihood {0}".format(name))

    def get_name_list(self) -> List[fit_plugin.Likelihood]:
        return [plugin.name for plugin in self.__found_plugins]


def start(
        data: FitData, options: minuit.Settings,
        functions: CallPackage, likelihood_name: str
):
    likelihood_loader = LikelihoodFetch()

    argument_translator = minuit.ParserObject(options.parameters)
    interface = _process_interface.FittingInterface(argument_translator)
    setup = likelihood_loader.get_likelihood(likelihood_name)

    likelihood = setup.get_likelihood(
        fit_plugin.OptimizerType.MINIMIZER, data, functions
    )


class Fitting(object):

    def start(self, data: FitData, optimizer_options: Settings):
        interface = _process_interface.FittingInterface(
            "Minimizer Argument Translator"
        )

        self.__setup_likelihood()
        self.__setup_processing()
        self.__set_interface()
        self.__start_optimizer()
        self.__finalize_program()

    def __setup_likelihood(self):

        self.__likelihood.setup_likelihood(
            self.__data_loader, self.__function_loader,
            self.__optimizer.get_optimizer_type(),
            {"generated length": self.__generated_length}
        )

    def __setup_processing(self):
        self.__processing.main_options(
            self.__likelihood.get_data(), self.__likelihood.get_likelihood(),
            self.__processing_interface
        )

    def __set_interface(self):
        self.__interface = self.__processing.fetch_interface()

    def __start_optimizer(self):
        self.__optimizer.run(
            self.__interface.run, self.__likelihood.LIKELIHOOD_TYPE
        )

    def __finalize_program(self):
        self.__interface.stop()
        self.__optimizer.save_data(self.__save_name)

    def save_data(self, save_location):
        self.__optimizer.save_data(save_location)
