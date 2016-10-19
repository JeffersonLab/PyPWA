import numpy

import io
import random
import time

from PyPWA.core_libs import plugin_loader
from PyPWA.core_libs.templates import plugin_templates
from PyPWA.core_libs.templates import interface_templates


class Simulator(plugin_templates.ShellMain):

    def __init__(
            self, data_parser=None, kernel_processing=None,
            the_type=None, functions_location=None,
            processing_name=None, setup_name=None, data_location=None,
            parameters=None, max_intensity=None, save_name=None,
            options=None
    ):
        """

        Args:
            data_parser (plugin_templates.DataParserTemplate):
            kernel_processing (plugin_templates.KernelProcessingTemplate):
            the_type (str):
            functions_location (str):
            processing_name (str):
            setup_name (str):
            data_location (str):
            parameters (dict):
            max_intensity (numpy.float64):
            save_name (str):
            options (dict):
        """

        self._data_parser = data_parser
        self._kernel_processing = kernel_processing
        self._the_type = the_type
        self._functions_location = functions_location
        self._processing_name = processing_name
        self._setup_name = setup_name
        self._data_location = data_location
        self._intensities = False
        self._rejection_list = False
        self._parameters = parameters
        self._max_intensity = max_intensity
        self._save_name = save_name

        if options:
            super(Simulator, self).__init__(options)

        self._raw_data = {}
        self._intensities = None  # type: numpy.ndarray

    def start(self):
        if self._the_type == "full" or self._the_type == "intensities":
            self._calc_intensities()
        if self._the_type == "full" or self._the_type == "weighting":
            self._rejection_method()

        if self._the_type == "intesities":
            self._data_parser.write(
                self._intensities, self._save_name + "_intensities.txt"
            )

            with io.open(self._save_name + "_max.txt") as stream:
                stream.write(str(self._max_intensity))

        elif self._the_type == "weighting" or self._the_type == "full":
            self._data_parser.write(
                self._rejection_list,
                self._save_name + "_rejection.txt"
            )

    def _calc_intensities(self):
        loader = plugin_loader.SingleFunctionLoader(
            self._functions_location
        )

        processing = loader.fetch_function(self._processing_name)
        setup = loader.fetch_function(self._setup_name)

        self._raw_data["data"] = self._data_parser.parse(
            self._data_location
        )

        the_kernel = IntensityKernel(setup, processing, self._parameters)
        the_interface = IntensityInterface()

        self._kernel_processing.main_options(
            self._raw_data, the_kernel, the_interface
        )

        operational_interface = self._kernel_processing.fetch_interface()
        self._intensities, self._max_intensity = operational_interface.run()

    def _rejection_method(self):
        if not self._intensities:
            self._intensities = self._data_parser.parse(self._data_location)

        the_random = random.SystemRandom(time.gmtime())

        weighted_list = self._intensities / self._max_intensity
        rejection = numpy.zeros(shape=len(weighted_list), dtype=bool)
        for index, event in enumerate(rejection):
            if event > the_random.random():
                rejection[index] = True

        self._rejection_list = rejection


class IntensityInterface(interface_templates.AbstractInterface):

    is_duplex = False

    def run(self, communicator, args):
        """

        Args:
            communicator (list):
            args:

        Returns:

        """

        final_array = numpy.zeros(len(communicator))

        for communication in communicator:
            data = communication.recv()
            final_array[data[0]] = data[1]

        return [final_array, final_array.max()]


class IntensityKernel(interface_templates.AbstractKernel):

    def __init__(self, setup_function, processing_function, parameters):
        """

        Args:
            setup_function:
            processing_function:
            parameters:
        """
        self._setup_function = setup_function
        self._processing_function = processing_function
        self._parameters = parameters
        self.data = None  # type: numpy.ndarray

    def setup(self):
        self._setup_function()

    def process(self, data=False):
        return [
            self.processor_id,
            self._processing_function(self._parameters, self.data)
            ]
