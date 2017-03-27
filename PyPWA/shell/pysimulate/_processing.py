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

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import internals

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class IntensityInterface(internals.KernelInterface):

    is_duplex = False
    __logger = logging.getLogger(__name__ + "IntensityInterface")

    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())

    def run(self, communicator, args):
        data = self.__receive_data(communicator)
        return self.__process_data(data)

    def __receive_data(self, communicator):
        list_of_data = list(range(len(communicator)))

        for communication in communicator:
            data = communication.receive()
            self.__logger.debug("Received data: " + repr(data))
            list_of_data[data[0]] = data[1]

        return list_of_data

    def __process_data(self, list_of_data):
        final_array = numpy.concatenate(list_of_data)
        self.__logger.debug("Final Array: " + repr(final_array))
        return [final_array, final_array.max()]


class IntensityKernel(internals.Kernel):

    data = None  # type: numpy.ndarray
    __setup_function = None  # type: function
    __processing_function = None  # type: function
    __parameters = None  # type: dict

    def __init__(self, setup_function, processing_function, parameters):
        self.__setup_function = setup_function
        self.__processing_function = processing_function
        self.__parameters = parameters

    def setup(self):
        self.__setup_function()

    def process(self, data=False):
        calculated_data = self.__processing_function(
            self.data, self.__parameters
        )

        return [self.processor_id, calculated_data]
