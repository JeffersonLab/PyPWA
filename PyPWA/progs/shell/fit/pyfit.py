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

from typing import List

from PyPWA.progs.shell.fit import interfaces
from PyPWA.progs.shell.fit._process_interface import FittingInterface

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared import plugin_loader
from PyPWA.core.shared.interfaces import internals
from PyPWA.core.shared.interfaces import plugins
from PyPWA.progs.shell.fit import likelihoods

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class LikelihoodPackager(object):

    def __init__(self):
        self.__plugin_search = plugin_loader.PluginLoader()
        self.__plugin_search.add_plugin_location(likelihoods)

    def get_likelihood(self, name):
        # type: (str) -> interfaces.Setup
        likelihood_list = self.__get_likelihoods()
        return self.__get_likelihood_by_name(likelihood_list, name)

    def __get_likelihoods(self):
        # type: () -> List[type(interfaces.Setup)]
        return self.__plugin_search.get_by_class(interfaces.Setup)

    def __get_likelihood_by_name(self, potential_likelihoods, name):
        # type: (List[type(interfaces.Setup)], str) -> interfaces.Setup
        for likelihood in potential_likelihoods:
            if likelihood.NAME == name:
                return likelihood
        self.__failed_to_find_likelihood(name)

    @staticmethod
    def __failed_to_find_likelihood(name):
        # type: (str) -> None
        raise ValueError("Failed to find likelihood: %s" % name)

    def get_likelihood_name_list(self):
        # type: () -> List[str]
        names = []
        for likelihood in self.__get_likelihoods():
            names.append(likelihood.NAME)
        return names


class Fitting(plugins.Main):

    def __init__(
            self,
            optimizer,  # type: plugins.Optimizer
            kernel_processing,  # type: plugins.KernelProcessing
            data_loader,  # type: loaders.DataLoading
            function_loader,  # type: loaders.FunctionLoader
            likelihood_type,  # type: str
            generated_length,  # type: int
            save_name  # type: str
    ):
        self.__optimizer = optimizer
        self.__processing = kernel_processing
        self.__data_loader = data_loader
        self.__function_loader = function_loader
        self.__likelihood_type = likelihood_type
        self.__generated_length = generated_length
        self.__save_name = save_name

        self.__likelihood_loader = LikelihoodPackager()
        self.__process_interface = None  # type: FittingInterface
        self.__likelihood = None  # type: interfaces.Setup
        self.__interface = None  # type: internals.ProcessInterface

    def start(self):
        self.__setup_interface()
        self.__setup_likelihood()
        self.__setup_processing()
        self.__set_interface()
        self.__start_optimizer()
        self.__finalize_program()

    def __setup_interface(self):
        self.__processing_interface = FittingInterface(
            self.__optimizer.return_parser()
        )

    def __setup_likelihood(self):
        self.__likelihood = self.__likelihood_loader.get_likelihood(
            self.__likelihood_type
        )

        self.__likelihood.setup_likelihood(
            self.__data_loader, self.__function_loader,
            {"generated length": self.__generated_length}
        )

    def __setup_processing(self):
        self.__processing.main_options(
            self.__likelihood.get_data(), self.__likelihood.get_likelihood(),
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
