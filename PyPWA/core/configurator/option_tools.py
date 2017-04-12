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
A collection of tools needed to help with options metadata.
-----------------------------------------------------------
The tools here are all simple enough to exist on their own, but all serve 
the purpose of helping with options metadata.

- CommandOptions - The object that is loaded wih values from the 
  configuration file that is then passed to the plugins setup.
  
- PluginsNamesConversion - Since the plugins are defined using an 
  enumeration, this object takes an enumeration and returns its readable 
  name, or takes a readable name and returns the enumeration.
"""

import logging
import re

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import options

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class CommandOptions(object):

    __logger = logging.getLogger(__name__ + ".CommandOptions")

    def __init__(self, default_options, loaded_options):
        self.__logger.addHandler(logging.NullHandler())
        self.__set_variables(default_options)
        self.__set_variables(loaded_options)

    def __set_variables(self, plugin_options):
        for key in list(plugin_options.keys()):
            name = self.__find_variable_name(key)
            setattr(self, name, plugin_options[key])

    def __find_variable_name(self, key):
        underscored_name = key.replace(" ", "_")
        lowercase_name = underscored_name.lower()
        filtered_name = re.sub(r'[^a-z0-9_]', '', lowercase_name)
        self.__logger.debug("Converted {0} to {1}".format(key, filtered_name))
        return filtered_name


class PluginNameConversion(object):
    __NAMES = [
        # Internal name, External Name
        [options.Types.DATA_PARSER, "Data Parsing"],
        [options.Types.DATA_READER, "Data Iterator"],
        [options.Types.KERNEL_PROCESSING, "Kernel Processor"],
        [options.Types.OPTIMIZER, "Optimizer"]
    ]

    def internal_to_external(self, plugin_type):
        for internal_name, external_name in self.__NAMES:
            if internal_name == plugin_type:
                return external_name

    def external_to_internal(self, plugin_type):
        for internal_name, external_name in self.__NAMES:
            if external_name == plugin_type:
                return internal_name
