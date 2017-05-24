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
Takes the options from OptionsObject and parses those options into 
NestedSampling. Also contains the reference function for Nestle's Prior.
"""

import logging
from typing import Callable

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.nestle import nested
from PyPWA.core.configurator import option_tools
from PyPWA.core.configurator import options

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class NestleSetup(options.Setup):

    __LOGGER = logging.getLogger(__name__ + ".NestleSetup")

    def __init__(self, options_object):
        # type: (option_tools.CommandOptions) -> None
        self.__options = options_object
        self.__loader = nested.LoadPrior()

        self.__prior = None  # type: Callable[[numpy.ndarray], numpy.ndarray]
        self.__minimizer = None  # type: nested.NestledSampling

        self.__load_prior()
        self.__set_minimizer()

    def __load_prior(self):
        self.__loader.load_prior(
            self.__options.prior_location, self.__options.prior_name
        )
        self.__prior = self.__loader.prior

    def __set_minimizer(self):
        self.__minimizer = nested.NestledSampling(
            self.__prior, self.__options.ndim, self.__options.npoints,
            self.__options.method, self.__options.update_interval,
            self.__options.npdim, self.__options.maxiter,
            self.__options.maxcall, self.__options.dlogz,
            self.__options.decline_factor
        )

    def return_interface(self):
        # type: () -> nested.NestledSampling
        return self.__minimizer


class NestlePriorFunction(options.FileBuilder):
    imports = set()
    functions = [
        """
def prior(x):
    # type: Callable[[numpy.ndarray], numpy.ndarray]
    # For information about how to use nestle's prior function, please read
    # nestle's documentation at: http://kylebarbary.com/nestle/index.html
    return x
        """
    ]
