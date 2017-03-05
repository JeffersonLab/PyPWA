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

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.builtin_plugins.nestle import nested
from PyPWA.core.configurator import options

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class NestleSetup(options.Setup):

    __logger = logging.getLogger("NestleSetup." + __name__)
    __loader = nested.LoadPrior()

    __interface = None  # type: NestledSampling()
    __options = None  # type: PyPWA.core.configurator.options.CommandObject
    __prior = None  # type: typing.Any

    def __init__(self, options_object):
        self.__options = options_object
        self.__load_prior()
        self.__set_minimizer()

    def __load_prior(self):
        self.__loader.load_prior(
            self.__options.prior_location, self.__options.prior_name
        )

    def __set_minimizer(self):
        self.__interface = nested.NestledSampling(
            self.__prior, self.__options.ndim, self.__options.npoints,
            self.__options.method, self.__options.update_interval,
            self.__options.npdim, self.__options.maxiter,
            self.__options.maxcall, self.__options.dlogz,
            self.__options.decline_factor
        )

    def return_interface(self):
        return self.__interface
