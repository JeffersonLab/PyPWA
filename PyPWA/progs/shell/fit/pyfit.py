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
- _LikelihoodPackager - a simple object that searches the 'likelihoods'
  package for the user's selected likelihood.
- Fitting - defines the actual main logic for the program.
"""

from typing import List

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.initializers.configurator import options
from PyPWA.libs import plugin_loader, configuration_db
from PyPWA.libs.components.optimizers import gateway
from PyPWA.libs.components.process import foreman
from PyPWA.progs.shell import loaders
from PyPWA.progs.shell.fit import interfaces, likelihoods
from PyPWA.progs.shell.fit._process_interface import FittingInterface

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


class Fitting(options.StartProgram):

    def __init__(self):
        self.__db = configuration_db.Connector()
        self.__processing = foreman.CalculationForeman()
        self.__optimizer = gateway.FetchOptimizer()
        self.__function_loader = loaders.FunctionLoader()
        self.__data_loader = loaders.DataLoading()

        self.__likelihood_type = (
            self.__db.read("shell fitting method", "likelihood type")
        )
        self.__generated_length = (
            self.__db.read("shell fitting method", "generated length")
        )
        self.__save_name = (
            Path(self.__db.read("shell fitting method", "save name"))
        )

        self.__likelihood_loader = LikelihoodPackager()
        self.__process_interface = None  # type: FittingInterface
        self.__likelihood = None  # type: interfaces.Setup
        self.__interface = None  # type: kernel.ProcessInterface

    def start(self):
        self.__setup_interface()
        self.__setup_likelihood()
        self.__setup_processing()
        self.__set_interface()
        self.__start_optimizer()
        self.__finalize_program()

    def __setup_interface(self):
        self.__processing_interface = FittingInterface(
            self.__optimizer.get_parser_object()
        )

    def __setup_likelihood(self):
        self.__likelihood = self.__likelihood_loader.get_likelihood(
            self.__likelihood_type
        )

        self.__likelihood.setup_likelihood(
            self.__data_loader, self.__function_loader,
            self.__optimizer.get_optimizer_type(),
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
        self.__optimizer.run(
            self.__interface.run, self.__likelihood.LIKELIHOOD_TYPE
        )

    def __finalize_program(self):
        self.__interface.stop()
        self.__optimizer.save_data(self.__save_name)
