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
Needed objects for kernel processing.
-------------------------------------
These objects implement the internal interfaces for kernel processing so 
that Simulation's intensities calculations can be executed quicker.
"""

import logging
from typing import Any, Dict, List, Tuple

import numpy
from numpy import ndarray

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import internals

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class IntensityInterface(internals.KernelInterface):

    IS_DUPLEX = False
    __LOGGER = logging.getLogger(__name__ + "IntensityInterface")

    def run(self, communicator, args):
        # type: (List[Any], Any) -> Tuple[ndarray, float]
        data = self.__receive_data(communicator)
        return self.__process_data(data)

    def __receive_data(self, communicator):
        # type: (List[Any]) -> List[ndarray]
        list_of_data = list(range(len(communicator)))

        for communication in communicator:
            data = communication.receive()
            self.__LOGGER.debug("Received data: " + repr(data))
            list_of_data[data[0]] = data[1]

        return list_of_data

    def __process_data(self, list_of_data):
        # type: (List[ndarray]) -> Tuple[ndarray, float]
        final_array = numpy.concatenate(list_of_data)
        self.__log_final_array_statistics(final_array)
        return final_array, final_array.max()

    def __log_final_array_statistics(self, array):
        # type: (ndarray) -> None
        self.__LOGGER.debug("Final Array: " + repr(array))
        self.__LOGGER.info("Max Intensity: %f" % array.max())
        self.__LOGGER.info("Min Intensity: %f" % array.min())
        self.__LOGGER.info("Intensities Range: %f" % array.ptp())
        self.__LOGGER.info("Intensities STD: %f" % array.std())
        self.__LOGGER.info("Intensities Mean: %f" % array.mean())


class IntensityKernel(internals.Kernel):

    __LOGGER = logging.getLogger(__name__ + ".IntensityKernel")

    def __init__(
            self,
            setup_function,  # type: shell_types.users_setup
            processing_function,  # type: shell_types.users_processing
            parameters  # type: Dict[str, float]
    ):
        # type: (...) -> None
        self.__setup_function = setup_function
        self.__processing_function = processing_function
        self.__parameters = parameters
        self.data = None  # type: ndarray

    def setup(self):
        self.__setup_function()

    def process(self, data=False):
        # type: (Any) -> Tuple[int, ndarray]
        self.__LOGGER.debug("%d is alive!" % self.PROCESS_ID)
        calculated_data = self.__processing_function(
            self.data, self.__parameters
        )

        return self.PROCESS_ID, calculated_data
