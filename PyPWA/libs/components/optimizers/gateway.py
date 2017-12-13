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

"""

from PyPWA import AUTHOR, VERSION
from PyPWA.libs import configuration_db
from PyPWA.libs.components.optimizers import _plugin_fetcher
from PyPWA.libs.components.optimizers import opt_plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _Settings(object):

    def __init__(self):
        self.__db = configuration_db.Connector()
        self.__make_plugin_settings()

    def __make_plugin_settings(self):
        plugin_settings = self.__db.read("Optimizer", "configuration")
        plugin_settings["parameters"] = self.parameters
        self.__db.initialize_component(self.plugin_name, plugin_settings)

    @property
    def parameters(self):
        return self.__db.read("Optimizer", "parameters")

    @property
    def plugin_name(self):
        return self.__db.read("Optimizer", "selected optimizer")


class FetchOptimizer(opt_plugins.Optimizer):

    def __init__(self):
        self.__config = None  # type: opt_plugins.OptimizerConf
        self.__optimizer = None  # type: opt_plugins.Optimizer

        self.__settings = _Settings()
        self.__optimizer_requester = _plugin_fetcher.OptimizerFetcher()
        self.__load_optimizer()

    def __load_optimizer(self):
        self.__config = self.__optimizer_requester.get_optimizer_by_name(
            self.__settings.plugin_name
        )
        self.__optimizer = self.__config.get_optimizer()

    def run(self, calculation_function, fitting_type=None):
        self.__optimizer.run(calculation_function, fitting_type)

    def save_data(self, save_location):
        self.__optimizer.save_data(save_location)

    def get_parser_object(self):
        # type: () -> opt_plugins.OptionParser
        return self.__config.get_optimizer_parser()

    def get_optimizer_type(self):
        # type: () -> opt_plugins.Type
        return self.__config.get_optimizer_type()
