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

"""
Holds the various likelihood calculations.
"""

import numpy

from PyPWA.core_libs.templates import interface_templates

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _CoreProcessingKernel(interface_templates.AbstractKernel):

    def __init__(self, setup_function, processing_function):
        self._setup_function = setup_function
        self._processing_function = processing_function

    def setup(self):
        if self._setup_function:
            self._setup_function()

    def process(self, data=False):
        raise NotImplementedError


class ExtendedLikelihoodAmplitude(_CoreProcessingKernel):

    def __init__(
            self, setup_function, processing_function, generated_length
    ):
        super(ExtendedLikelihoodAmplitude, self).__init__(
           setup_function, processing_function
        )

        self._processed = 1.0/generated_length
        self.data = None  # type: numpy.ndarray
        self.monte_carlo = None  # type: numpy.ndarray
        self.qfactor = 1  # type: numpy.ndarray

    def process(self, data=False):
        processed_data = self._processing_function(self.data, data)
        processed_monte_carlo = self._processing_function(
            self.monte_carlo, data
        )
        return self._likelihood(processed_data, processed_monte_carlo)

    def _likelihood(self, data, accepted):
        """
        Calculates the extended likelihood function

        Args:
            data:
            accepted:
        """
        try:
            value = -(numpy.sum(self.qfactor * numpy.log(data))) + \
                     (self._processed * numpy.sum(accepted))
        except ZeroDivisionError:
            value = numpy.NaN

        return value


class UnextendedLikelihoodAmplitude(_CoreProcessingKernel):

    def __init__(self, setup_function, processing_function):
        super(UnextendedLikelihoodAmplitude, self).__init__(
            setup_function, processing_function
        )

        self.data = None     # type: numpy.ndarray
        self.qfactor = 1  # type: numpy.ndarray
        self.binned = 1   # type: numpy.ndarray

    def process(self, data=False):
        processed_data = self._processing_function(self.data, data)
        return self._likelihood(processed_data)

    def _likelihood(self, data):
        """
        Calculates the binned likelihood function

        Args:
            data:
        """
        value = -(
            numpy.sum(self.qfactor * self.binned * numpy.log(data))
        )
        return value


class Chi(_CoreProcessingKernel):

    def __init__(self, setup_function, processing_function):
        super(Chi, self).__init__(setup_function, processing_function)

        self.data = None  # type: numpy.ndarray
        self.binned = None  # type: numpy.ndarray

    def process(self, data=False):
        processed_data = self._processing_function(self.data, data)
        return self._likelihood(processed_data)

    def _likelihood(self, data):
        """
        Calculates the ChiSquare function

        Args:
            data:
        """
        return ((data - self.binned)**2) / self.binned


class FittingInterfaceKernel(interface_templates.AbstractInterface):

    is_duplex = True

    def __init__(self, minimizer_function):
        """

        Args:
            minimizer_function (interface_templates.MinimizerParserTemplate):
        """
        self._parameter_parser = minimizer_function

    def run(self, communication, *args):
        """
        This is the function is called by minuit and acts as a wrapper for
        the users function

        Args:
            communication: Communication Pipes
            *args: The parameters in list format

        Returns:
            float: The final value from the likelihood function
        """

        parsed_arguments = self._parameter_parser.convert(args)

        for pipe in communication:
            pipe.send(parsed_arguments)

        values = numpy.zeros(shape=len(communication))

        for index, pipe in enumerate(communication):
            values[index] = pipe.recieve()

        return numpy.sum(values)
