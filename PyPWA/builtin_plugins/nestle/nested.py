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

import logging

import nestle
import typing

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.nestle import _graph_data
from PyPWA.core.shared import plugin_loader
from PyPWA.core.shared.interfaces import internals
from PyPWA.core.shared.interfaces import plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _NestleParserObject(internals.MinimizerOptionParser):

    def convert(self, *args):
        return args[0][0]


class NestledSampling(plugins.Optimizer):

    __logger = logging.getLogger(__name__)
    __callback_object = None  # type: _graph_data.SaveData
    __results = None  # type: nestle.Result

    __calc_function = None  # type: typing.Any
    __prior = None  # type: typing.Any
    __npdim = None  # type: int
    __ndim = None  # type: int
    __npoints = None  # type: int
    __method = None  # type: str
    __update_interval = None  # type: int
    __maxiter = None  # type: int
    __maxcall = None  # type: int
    __dlogz = None  # type: float
    __decline_factor = None  # type: float
    __folder_location = False  # type: str

    def __init__(
            self, prior, ndim, npoints=100, method="single",
            update_interval=None, npdim=None, maxiter=None, maxcall=None,
            dlogz=None, decline_factor=None, folder_location=False
    ):
        self.__logger.addHandler(logging.NullHandler())
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

    def main_options(self, calc_function, fitting_type=False):
        self.__calc_function = calc_function

    def start(self):
        self.__start_sampling()

    def __setup_callback(self):
        if self.__folder_location:
            self.__callback_object = _graph_data.SaveData(
                self.__folder_location
            )

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
            callback=self.__callback_object.process_callback
        )

    def return_parser(self):
        return _NestleParserObject()

    def save_extra(self, save_name):
        print(self.__results.summary())


class LoadPrior(object):

    __logger = logging.getLogger("_LoadPrior." + __name__)
    __plugin_storage = plugin_loader.PluginStorage()
    __found_prior = None  # type: typing.Any

    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())

    def load_prior(self, prior_location, prior_name):
        self.__add_prior_location(prior_location)
        self.__set_prior(prior_name)

    def __add_prior_location(self, location):
        self.__plugin_storage.add_plugin_location(location)

    def __set_prior(self, name):
        self.__found_prior = self.__plugin_storage.get_by_name(name)

    @property
    def prior(self):
        return self.__found_prior
