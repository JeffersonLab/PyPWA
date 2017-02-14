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

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core import plugin_loader
from PyPWA.core.templates import interface_templates
from PyPWA.core.templates import plugin_templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _NestleParserObject(interface_templates.MinimizerParserTemplate):

    def convert(self, *args):
        return args[0][0]


class NestledSampling(plugin_templates.MinimizerTemplate):

    _logger = logging.getLogger(__name__)

    _loaded_function = None  # type: typing.Any

    _calc_function = None  # type: typing.Any
    _prior_location = None  # type: str
    _prior_name = None  # type: str
    _ndim = None  # type: int
    _npoints = None  # type: int
    _method = None  # type: str
    _update_interval = None  # type: int
    _npdim = None  # type: int
    _maxiter = None  # type: int
    _maxcall = None  # type: int
    _dlogz = None  # type: float
    _decline_factor = None  # type: float

    def __init__(
            self, calc_function=False, prior_location=None,
            prior_name=None, ndim=None, npoints=None, method=None,
            update_interval=None, npdim=None, maxiter=None, maxcall=None,
            dlogz=None, decline_factor=None, **options
    ):
        self._logger.addHandler(logging.NullHandler())

        self._calc_function = calc_function
        self._prior_location = prior_location
        self._prior_name = prior_name
        self._ndim = ndim
        self._npoints = npoints
        self._method = method
        self._update_interval = update_interval
        self._npdim = npdim
        self._maxiter = maxiter
        self._maxcall = maxcall
        self._dlogz = dlogz
        self._decline_factor = decline_factor

        if options:
            super(NestledSampling, self).__init__(options)

    def main_options(self, calc_function, fitting_type=False):
        self._calc_function = calc_function

    def start(self):
        self._load_prior()
        self._start_sampling()

    def _load_prior(self):
        loader = plugin_loader.PythonSheetLoader(
            self._prior_location
        )
        self._loaded_function = loader.fetch_function(
            self._prior_name, True
        )

    def _start_sampling(self):
        nestle.sample(
            loglikelihood=self._calc_function,
            prior_transform=self._loaded_function,
            ndim=self._ndim,
            npoints=self._npoints,
            method=self._method,
            update_interval=self._update_interval,
            npdim=self._npdim,
            maxiter=self._maxiter,
            maxcall=self._maxcall,
            dlogz=self._dlogz,
            decline_factor=self._decline_factor
        )

    def return_parser(self):
        return _NestleParserObject()

    def save_extra(self, save_name):
        pass  # We are still learning how nestle works..

