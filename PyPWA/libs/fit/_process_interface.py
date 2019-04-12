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
Processing and Output
---------------------
This is where the processing interface is defined along with the automated
output from the the parallel thread.

- _ThreadInterface - The object between the main thread and the output thread.

- _OutputThread - The actual output thread, its started with each call to the
  likelihood. Has a 1hz output rate.

- FittingInterface - The interface between the Likelihood Kernels and the
  optimizer module.
"""

from __future__ import print_function

import time

import logging
import numpy
import threading
from typing import List

from PyPWA import queue, AUTHOR, VERSION
from PyPWA.libs.components import process

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class FittingInterface(process.Interface):

    IS_DUPLEX: bool = True
    __LOGGER = logging.getLogger(__name__ + ".FittingInterface")

    def __init__(self, parameter_translator):
        self.__parameter_parser = parameter_translator
        self.__thread_interface = _ThreadInterface()
        self.__thread_interface.start()

    def run(self, communication, *args):
        start_of_call = time.time()

        self.__send_arguments(communication, args)
        final_value = self.__get_final_value(communication)

        time_of_call = time.time() - start_of_call

        self.__thread_interface.send_new_values(final_value, time_of_call)

        return final_value

    def __send_arguments(self, communication, args):
        parsed_arguments = self.__parameter_parser.convert(args)

        for pipe in communication:
            pipe.send(parsed_arguments)

    @staticmethod
    def __get_final_value(communication):
        values = numpy.zeros(shape=len(communication))
        for index, pipe in enumerate(communication):
            values[index] = pipe.recv()
        return numpy.sum(values)

    def shutdown_thread(self):
        self.__thread_interface.stop()


class _ThreadInterface(object):

    __LOGGER = logging.getLogger(__name__ + "_ThreadInterface")

    def __init__(self):
        self.__send_queue = queue.Queue()
        self.__enabled = self.__get_is_enabled()

    def __get_is_enabled(self) -> bool:
        if not logging.getLogger().isEnabledFor(logging.INFO):
            return True
        else:
            self.__LOGGER.info(
                "Processor Output is disabled while info logging is enabled"
            )
            return False

    def start(self):
        if self.__enabled:
            thread = _OutputThread(self.__send_queue)
            thread.start()

    def send_new_values(self, final_value: float, time_of_call: float):
        if self.__enabled:
            self.__send_queue.put((final_value, time_of_call))
        else:
            print("final_value is {0}".format(final_value))

    def stop(self):
        if self.__enabled:
            self.__send_queue.put(0)


class _OutputThread(threading.Thread):

    def __init__(self, receive_queue: queue.Queue):
        super(_OutputThread, self).__init__()
        self.__receive_queue = receive_queue
        self.__output_pulse = "-"
        self.__start_time = time.time()
        self.daemon = True

    def run(self):
        times = []
        last_value = 0
        while True:
            if self.__receive_queue.empty():
                self.__output(times, last_value)
                time.sleep(.2)
            else:
                result = self.__receive_queue.get()
                if result == 0:
                    break
                last_value = result[0]
                times.append(result[1])

    def __output(self, times: List[float], last_value: float):
        output = self.__create_output(times, last_value)
        print(output, end="\r")

    def __create_output(self, times: List[float], last_value: float) -> str:
        if len(times):
            return self.__simple_output()
        else:
            return self.__full_output(times, last_value)

    def __simple_output(self) -> str:
        runtime = self.__get_total_runtime()
        return "Elapsed time: {0: .2f} {1}".format(runtime, self.__pulse())

    def __full_output(self, times: List[float], last_value: float) -> str:
        output = (
            "Last Value: {0: .3f}, Average Time: {1: .2f}, "
            "Total Runtime {3: .2f} {4}"
        )
        return output.format(
            last_value, numpy.mean(times),
            self.__get_total_runtime(), self.__pulse()
        )

    def __get_total_runtime(self) -> float:
        return time.time() - self.__start_time

    def __pulse(self) -> str:
        if self.__output_pulse is "-":
            self.__output_pulse = "/"
        elif self.__output_pulse is "/":
            self.__output_pulse = "\\"
        elif self.__output_pulse is "\\":
            self.__output_pulse = "-"
        return self.__output_pulse
