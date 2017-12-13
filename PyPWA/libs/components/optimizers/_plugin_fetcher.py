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

"""

from typing import List

from PyPWA import AUTHOR, VERSION, builtin_plugins
from PyPWA.libs import plugin_loader
from PyPWA.libs.components.optimizers import opt_plugins as templates

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class OptimizerFetcher(object):

    def __init__(self):
        self.__loader = plugin_loader.PluginLoader()
        self.__loader.add_plugin_location(builtin_plugins)
        self.__configs = None  # type: List[templates.OptimizerConf]
        self.__load_optimizers()

    def __load_optimizers(self):
        self.__configs = self.__loader.get_by_class(
            templates.OptimizerConf
        )

    def get_optimizer_by_name(self, name):
        for configuration in self.__configs:
            if configuration.name == name:
                return configuration

        raise ValueError(
            "%s not found! Only found %s!" % (
                name, str(self.get_list_of_plugins())
            )
        )

    def get_list_of_plugins(self):
        name_list = []
        for configuration in self.__configs:
            name_list.append(configuration.name)
        return name_list

    def get_plugin_types(self):
        types = dict()
        for configuration in self.__configs:
            types.update(configuration.get_types())
        return types


class AllOptions(templates.OptimizerConf):

    def __init__(self):
        self.name = "None selected"
        self.__defaults = dict()

        self.__loader = plugin_loader.PluginLoader()
        self.__loader.add_plugin_location(builtin_plugins)


    def __process_optimizers(self):
        configurations = self.__loader.get_by_class(templates.OptimizerConf)
        for configuration in configurations:
            self.__defaults.update(configuration.get_defaults())


    def get_defaults(self):
        return self.__defaults
