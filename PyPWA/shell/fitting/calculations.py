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

from __future__ import print_function

import logging
import threading
import time

try:
    from queue import Queue
except ImportError:
    from Queue import Queue

import numpy
from PyPWA import VERSION, LICENSE, STATUS
from core.shared.interfaces import internals

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _CoreProcessingKernel(internals.AbstractKernel):

    def __init__(self, setup_function, processing_function):
        """

        Args:
            setup_function:
            processing_function:
        """
        self._setup_function = setup_function
        self._processing_function = processing_function

    def setup(self):
        """

        Returns:

        """
        if self._setup_function:
            self._setup_function()

    def process(self, data=False):
        """

        Args:
            data:

        Returns:

        """
        raise NotImplementedError


class ExtendedLikelihoodAmplitude(_CoreProcessingKernel):

    def __init__(
            self, setup_function, processing_function, generated_length
    ):
        """

        Args:
            setup_function:
            processing_function:
            generated_length:
        """
        super(ExtendedLikelihoodAmplitude, self).__init__(
           setup_function, processing_function
        )

        self._processed = 1.0/generated_length
        self.data = None  # type: numpy.ndarray
        self.monte_carlo = None  # type: numpy.ndarray
        self.qfactor = 1  # type: numpy.ndarray

    def process(self, data=False):
        """

        Args:
            data:

        Returns:

        """
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
        if numpy.any(data == 0):
            print("WARNING, Found Zeros! " + repr(
                numpy.count_nonzero(data == 0)
            ))
        value = -(numpy.sum(self.qfactor * numpy.log(data))) + \
                 (self._processed * numpy.sum(accepted))

        return value


class UnextendedLikelihoodAmplitude(_CoreProcessingKernel):

    def __init__(self, setup_function, processing_function):
        """

        Args:
            setup_function:
            processing_function:
        """
        super(UnextendedLikelihoodAmplitude, self).__init__(
            setup_function, processing_function
        )

        self.data = None     # type: numpy.ndarray
        self.qfactor = 1  # type: numpy.ndarray
        self.binned = 1   # type: numpy.ndarray

    def process(self, data=False):
        """

        Args:
            data:

        Returns:

        """
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
        """

        Args:
            setup_function:
            processing_function:
        """
        super(Chi, self).__init__(setup_function, processing_function)

        self.data = None  # type: numpy.ndarray
        self.binned = None  # type: numpy.ndarray

    def process(self, data=False):
        """

        Args:
            data:

        Returns:

        """
        processed_data = self._processing_function(self.data, data)
        return self._likelihood(processed_data)

    def _likelihood(self, data):
        """
        Calculates the ChiSquare function

        Args:
            data:
        """
        return ((data - self.binned)**2) / self.binned


class FittingInterfaceKernel(internals.AbstractInterface):

    is_duplex = True

    def __init__(self, minimizer_function):
        """

        Args:
            minimizer_function (interface_templates.MinimizerParserTemplate):
        """
        self._logger = logging.getLogger(__name__)

        self._parameter_parser = minimizer_function
        self._last_value = None
        self._send_queue = Queue()
        self._receive_queue = Queue()
        self._times = []
        self._thread = None

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
        self._output_handler()

        parsed_arguments = self._parameter_parser.convert(args)

        for pipe in communication:
            pipe.send(parsed_arguments)

        values = numpy.zeros(shape=len(communication))

        for index, pipe in enumerate(communication):
            values[index] = pipe.receive()

        final_value = numpy.sum(values)
        self._last_value = final_value
        self._output_handler(True)
        self._logger.info("Final Value is: %f15" % final_value)
        return final_value

    def _output_handler(self, end=False):
        """

        Args:
            end:

        Returns:

        """
        if end:
            self._kill_thread()
        else:
            self._create_thread()

    def _kill_thread(self):
        """

        Returns:

        """
        self._send_queue.put("die")
        self._times.append(float(self._receive_queue.get()))

    def _average_time(self):
        """

        Returns:

        """
        if len(self._times) > 0:
            return sum(self._times) / len(self._times)
        else:
            return 0

    def _create_thread(self):
        """

        Returns:

        """
        if len(self._times) == 0:
            last_time = 0
        else:
            last_time = self._times[-1]

        self._thread = OutputThread(
            self._receive_queue, self._send_queue,
            self._last_value, last_time, self._average_time()
        )
        self._thread.start()


class OutputThread(threading.Thread):

    def __init__(
            self, send_queue, receive_queue, last_value,
            last_time, average_time
    ):
        """

        Args:
            send_queue:
            receive_queue:
            last_value:
            last_time:
            average_time:
        """
        self._output_pulse = "-"
        self._send_queue = send_queue
        self._receive_queue = receive_queue
        self._last_value = last_value
        self._last_time = last_time
        self._average_time = average_time
        self._initial_time = time.time()
        super(OutputThread, self).__init__()

    def _pulse(self):
        """

        Returns:

        """
        if self._output_pulse is "-":
            self._output_pulse = "/"
        elif self._output_pulse is "/":
            self._output_pulse = "\\"
        elif self._output_pulse is "\\":
            self._output_pulse = "-"

    def _create_output(self):
        """

        Returns:

        """
        self._pulse()

        current_time = time.time() - self._initial_time

        if isinstance(self._last_value, type(None)):
            string = "Elapsed time: {0:.2f} {1}".format(
                current_time, self._output_pulse
            )
        else:
            string = "Last Value: {0}, Average Time: {1:.4f}, " \
                     "Elapsed Time: {2:.2f} {3}".format(
                      self._last_value, self._average_time,
                      current_time, self._output_pulse
                      )

        return string

    def _return_time(self):
        """

        Returns:

        """
        self._receive_queue.get()
        current_time = time.time() - self._initial_time
        self._send_queue.put(current_time)

    def run(self):
        """

        Returns:

        """
        while True:
            if not self._receive_queue.empty():
                self._return_time()
                break
            time.sleep(.05)
            print("\r" + self._create_output(), end="\r")
