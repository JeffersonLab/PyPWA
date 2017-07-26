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
from typing import Any, Callable, Tuple
from typing import Optional as Opt

import nestle
import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.nestle import _graph_data
from PyPWA.builtin_plugins.nestle import _save_results
from PyPWA.libs import plugin_loader
from PyPWA.libs.interfaces import optimizers

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _NestleParserObject(optimizers.OptimizerOptionParser):

    def convert(self, *args):
        # type: (Tuple[Tuple[Tuple[numpy.ndarray]]]) -> numpy.ndarray
        return args[0][0][0]


class NestledSampling(optimizers.Optimizer):

    OPTIMIZER_TYPE = optimizers.OptimizerTypes.MAXIMIZER

    __LOGGER = logging.getLogger(__name__ + ".NestledSampling")

    def __init__(
            self,
            prior,  # type: Callable[[numpy.ndarray], numpy.ndarray]
            ndim,  # type: int
            npoints=100,   # type: int
            method="single",  # type: str
            update_interval=None,   # type: Opt[int]
            npdim=None,   # type: Opt[int]
            maxiter=None,  # type: Opt[int]
            maxcall=None,  # type: Opt[int]
            dlogz=None,   # type: Opt[float]
            decline_factor=None,  # type: Opt[float]
            folder_location=False  # type: Opt[str]
    ):
        # type: (...) -> None
        self.__save_data = _save_results.SaveData()
        self.__prior = prior
        self.__ndim = ndim
        self.__npoints = npoints
        self.__method = method
        self.__update_interval = update_interval
        self.__npdim = npdim
        self.__maxiter = maxiter
        self.__maxcall = maxcall
        self.__dlogz = dlogz
        self.__decline_factor = decline_factor
        self.__folder_location = folder_location
        self.__calc_function = None  # type: Callable[[Any], float]
        self.__callback_object = None  # type: _graph_data.SaveData
        self.__results = None  # type: nestle.Result

    def main_options(self, calc_function, fitting_type=False):
        # type: (Callable[[Any], float], optimizers.LikelihoodTypes) -> None
        self.__calc_function = calc_function

    def start(self):
        self.__start_sampling()

    def __setup_callback(self):
        if self.__folder_location:
            self.__LOGGER.info("Writing nestle's data to disk.")
            callback = _graph_data.SaveData(self.__folder_location)
            self.__callback_object = callback.process_callback

    def __start_sampling(self):
        self.__results = nestle.sample(
            loglikelihood=self.__calc_function,
            prior_transform=self.__prior,
            ndim=self.__ndim,
            npoints=self.__npoints,
            method=self.__method,
            update_interval=self.__update_interval,
            npdim=self.__npdim,
            maxiter=self.__maxiter,
            maxcall=self.__maxcall,
            dlogz=self.__dlogz,
            decline_factor=self.__decline_factor,
            callback=self.__callback_object
        )

    def return_parser(self):
        # type: () -> _NestleParserObject
        return _NestleParserObject()

    def save_extra(self, save_name):
        self.__save_data.save_data(save_name, self.__results)


class LoadPrior(object):

    __LOGGER = logging.getLogger("_LoadPrior." + __name__)

    def __init__(self):
        self.__plugin_storage = plugin_loader.PluginLoader()
        self.__found_prior = None  # type: Any


    def load_prior(self, prior_location, prior_name):
        # type: (str, str) -> None
        self.__add_prior_location(prior_location)
        self.__set_prior(prior_name)

    def __add_prior_location(self, location):
        # type: (str) -> None
        self.__plugin_storage.add_plugin_location(location)

    def __set_prior(self, name):
        # type: (str) -> None
        self.__found_prior = self.__plugin_storage.get_by_name(name)

    @property
    def prior(self):
        # type: () -> Callable[[numpy.ndarray], numpy.ndarray]
        return self.__found_prior
