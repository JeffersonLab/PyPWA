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

import logging

from PyPWA.core.configurator.storage import core_storage
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ModulePicking(object):

    __logger = logging.getLogger(__name__)
    __module_storage = None  # type: core_storage.ModuleStorage

    def __init__(self, extra_locations=None):
        self.__logger.addHandler(logging.NullHandler())
        self.__module_storage = core_storage.ModuleStorage(extra_locations)

    def request_main_by_id(self, the_id):
        for main in self.__module_storage.shell_modules:
            the_main = self.__safely_load_module(main)
            if not isinstance(the_main, type(None)):
                if the_main.plugin_name == the_id:
                    return the_main

    def request_plugin_by_name(self, name):
        for plugin in self.__module_storage.option_modules:
            the_plugin = self.__safely_load_module(plugin)
            if not isinstance(the_plugin, type(None)):
                if the_plugin.plugin_name == name:
                    return the_plugin

    def __safely_load_module(self, module):
        try:
            return module()
        except Exception as Error:
            self.__log_error(Error)

    def __log_error(self, error):
        self.__logger.error("Failed to load module!")
        self.__logger.exception(error)