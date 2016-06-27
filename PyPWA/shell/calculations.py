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

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ExtendedLikelihoodAmplitude(object):
    def __init__(self, generated_length):
        self._processed = 1.0/generated_length

    def likelihood(self, data, accepted, qfactor):
        """
        Calculates the extended likelihood function

        Args:
            data:
            accepted:
            qfactor:
        """
        try:
            value = -(numpy.sum(qfactor * numpy.log(data))) + (self._processed * numpy.sum(accepted))
        except ZeroDivisionError:
            value = numpy.NaN

        return value


class UnextendedLikelihoodAmplitude(object):

    @staticmethod
    def likelihood(data, binned, q_factor):
        """
        Calculates the binned likelihood function

        Args:
            data:
            binned:
            q_factor:
        """
        try:
            value = -(numpy.sum(q_factor * binned * numpy.log(data)))
        except ZeroDivisionError:
            value = numpy.NaN

        return value


class Chi(object):
    def likelihood(self, data, binned, qfactor):
        """
        Calculates the ChiSquare function

        Args:
            data:
            binned:
            qfactor:
        """
        masked_data = numpy.ma.masked_equal(data, 0)
        return ((masked_data - binned)**2) / binned


class FittingRunKernel(object):
    def __init__(self, num_processes, parameter_names):
        self._num_processes = num_processes
        self._parameter_names = parameter_names

    def run(self, coms, *args):
        """
        This is the function is called by minuit and acts as a wrapper for the \
        users function

        Args:
            *args: The parameters in list format

        Returns:
            float: The final value from the likelihood function
        """

        parameters_with_values = {}
        for parameter, arg in zip(self._parameter_names, args):
            parameters_with_values[parameter] = arg

        for pipe in coms:
            pipe.send(parameters_with_values)

        values = numpy.zeros(shape=self._num_processes)

        for index, pipe in enumerate(coms):
            values[index] = pipe.recieve()

        return numpy.sum(values)
