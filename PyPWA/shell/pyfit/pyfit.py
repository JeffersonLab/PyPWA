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
PyFit, a flexible python fitting utility.
-----------------------------------------

- _LikelihoodPackager - a simple object that searches the 'likehoods' 
  package for the user's selected likelihood.

- Fitting - defines the actual main logic for the program.
"""

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared import plugin_loader
from PyPWA.core.shared.interfaces import internals
from PyPWA.core.shared.interfaces import plugins
from PyPWA.shell import loaders
from PyPWA.shell.pyfit import _process_interface
from PyPWA.shell.pyfit import interfaces
from PyPWA.shell.pyfit import likelihoods

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _LikelihoodPackager(object):

    __plugin_search = plugin_loader.PluginLoader()

    def __init__(self):
        self.__plugin_search.add_plugin_location(likelihoods)

    def get_likelihood(self, name):
        likelihood_list = self.__get_likelihoods()
        return self.__get_likelihood_by_name(likelihood_list, name)

    def __get_likelihoods(self):
        return self.__plugin_search.get_by_class(interfaces.Setup)

    def __get_likelihood_by_name(self, potential_likelihoods, name):
        for likelihood in potential_likelihoods:
            if likelihood.name == name:
                return likelihood
        self.__failed_to_find_likelihood(name)

    @staticmethod
    def __failed_to_find_likelihood(name):
        raise ValueError("Failed to find likelihood: %s" % name)


class Fitting(plugins.Main):
    __optimizer = None  # type: plugins.Optimizer
    __processing = None  # type: plugins.KernelProcessing
    __data_loader = None  # type: loaders.DataLoading
    __function_loader = None  # type: loaders.FunctionLoader
    __likelihood_type = None  # type: str
    __generated_length = None  # type: int
    __save_name = None  # type: str

    __processing_interface = None  # type: _process_interface.FittingInterface
    __likelihood_loader = _LikelihoodPackager()
    __likelihood = None  # type: interfaces.Setup
    __interface = None  # type: internals.ProcessInterface

    def __init__(
            self, optimizer, kernel_processing, data_loader,
            function_loader, likelihood_type, generated_length,
            save_name
    ):
        self.__optimizer = optimizer
        self.__processing = kernel_processing
        self.__data_loader = data_loader
        self.__function_loader = function_loader
        self.__likelihood_type = likelihood_type
        self.__generated_length = generated_length
        self.__save_name = save_name

    def start(self):
        self.__load_nested_data()
        self.__setup_interface()
        self.__setup_likelihood()
        self.__setup_processing()
        self.__set_interface()
        self.__start_optimizer()
        self.__finalize_program()

    def __load_nested_data(self):
        print("Loading Data.")
        self.__data_loader.load_data()
        print("Loading Functions.")
        self.__function_loader.load_functions()

    def __setup_interface(self):
        self.__processing_interface = _process_interface.FittingInterface(
            self.__optimizer.return_parser()
        )

    def __setup_likelihood(self):
        likelihood = self.__likelihood_loader.get_likelihood(
            self.__likelihood_type
        )

        self.__likelihood = likelihood(
            self.__data_loader, self.__function_loader, {
                "Generated Length": self.__generated_length
            }
        )

    def __setup_processing(self):
        self.__processing.main_options(
            self.__likelihood.data, self.__likelihood.likelihood,
            self.__processing_interface
        )

    def __set_interface(self):
        self.__interface = self.__processing.fetch_interface()

    def __start_optimizer(self):
        self.__optimizer.main_options(
            self.__interface.run, self.__likelihood_type
        )
        self.__optimizer.start()

    def __finalize_program(self):
        self.__interface.stop()
        self.__optimizer.save_extra(self.__save_name)
