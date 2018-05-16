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
Multinest maximization
----------------------
A very accurate but slow optimizer that will try to find the maximas inside
your parameter space for provided function.

- _NestleParserObject - Removes any extra information from the prior before
  its passed to the kernels.
- NestedSampling - The actual optimizer object.
- LoadPrior - Loads the prior for the optimizer.
"""

import logging
from typing import Any, Callable, Tuple, Dict

import nestle
import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.nestle import _save_results, _settings
from PyPWA.libs import plugin_loader
from PyPWA.libs.components.optimizers import opt_plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION



class NestleParserObject(opt_plugins.OptionParser):

    def __init__(self):
        self.__parameters = _settings.NestleSettings().parameters

    def convert(self, *args):
        # type: (Tuple[Tuple[Tuple[numpy.ndarray]]]) -> Dict[str, numpy.ndarray]
        values = dict()
        for parameter, slice in zip(self.__parameters, args[0][0][0]):
            values[parameter] = slice
        return values


class _LoadPrior(object):

    __LOGGER = logging.getLogger("_LoadPrior." + __name__)

    def __init__(self):
        self.__plugin_storage = plugin_loader.PluginLoader()
        self.__settings = _settings.NestleSettings()
        self.__found_prior = None  # type: Any


    def load_prior(self):
        self.__add_prior_location()
        self.__set_prior()

    def __add_prior_location(self):
        self.__plugin_storage.add_plugin_location(
            self.__settings.prior_location
        )

    def __set_prior(self):
        self.__found_prior = self.__plugin_storage.get_by_name(
            self.__settings.prior_name
        )

    @property
    def prior(self):
        # type: () -> Callable[numpy.ndarray]
        return self.__found_prior


class NestledSampling(opt_plugins.Optimizer):

    __LOGGER = logging.getLogger(__name__ + ".NestledSampling")

    def __init__(self):
        self.__results = None  # type: nestle.Result
        self.__save_data = _save_results.SaveData()
        self.__settings = _settings.NestleSettings()
        self.__function = _LoadPrior()

    def run(self, calculation_function, fitting_type=None):
        self.__function.load_prior()
        self.__results = nestle.sample(
            loglikelihood=calculation_function,
            prior_transform=self.__function.prior,
            ndim=self.__settings.ndim,
            npoints=self.__settings.npoints,
            method=self.__settings.method,
            update_interval=self.__settings.update_interval,
            npdim=self.__settings.npdim,
            maxiter=self.__settings.maxiter,
            maxcall=self.__settings.maxcall,
            dlogz=self.__settings.dlogz,
            decline_factor=self.__settings.decline_factor
        )


    def save_extra(self, save_name):
        self.__save_data.save_data(save_name, self.__results)
