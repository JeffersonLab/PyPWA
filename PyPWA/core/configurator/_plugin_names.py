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

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core.configurator import options

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class PluginTypeName(object):
    __NAMES = [
        # Internal name, External Name
        [options.PluginTypes.DATA_PARSER, "Data Parsing"],
        [options.PluginTypes.DATA_READER, "Data Iterator"],
        [options.PluginTypes.KERNEL_PROCESSING, "Kernel Processor"],
        [options.PluginTypes.MINIMIZATION, "Minimizer"]
    ]

    def internal_to_external(self, plugin_type):
        for internal_name, external_name in self.__NAMES:
            if internal_name == plugin_type:
                return external_name

    def external_to_internal(self, plugin_type):
        for internal_name, external_name in self.__NAMES:
            if external_name == plugin_type:
                return internal_name

