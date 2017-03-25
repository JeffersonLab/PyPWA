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

from PyPWA.core.shared.interfaces import internals
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Likelihood(internals.Kernel):

    def __init__(self, setup_function, processing_function):
        self.__setup_function = setup_function
        self._processing_function = processing_function

    def setup(self):
        if self.__setup_function:
            self.__setup_function()

    def process(self, data=False):
        raise NotImplementedError


class Setup(object):
    name = NotImplemented
    _dictionary_data = None  # type: dict
    _likelihood = None  # type: Likelihood

    def setup_interface(self):
        raise NotImplementedError

    @property
    def likelihood(self):
        return self._likelihood

    @property
    def data(self):
        return self._dictionary_data