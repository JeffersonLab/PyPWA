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


class ModuleTemplates(object):
    """
    Parses the templates for all plugins and modules.
    """

    __logger = logging.getLogger(__name__)
    __plugin_storage = None  # type: core_storage.ModuleStorage
    __templates = None  # type: dict

    def __init__(self, extra_locations=False):
        self._plugin_storage = core_storage.ModuleStorage(extra_locations)
        self.__logger.addHandler(logging.NullHandler())
        self.__templates = {}
        self.__process_options()
        self.__process_main()

    def __process_options(self):
        for plugin in self._plugin_storage.option_modules:
            loaded = self.__safely_load_module(plugin)
            if not isinstance(loaded, type(None)):
                self.__add_option_module(loaded)

    def __process_main(self):
        for main in self._plugin_storage.shell_modules:
            loaded = self.__safely_load_module(main)
            if not isinstance(loaded, type(None)):
                self.__add_main_module(loaded)

    def __safely_load_module(self, module):
        try:
            return module()
        except Exception as Error:
            self.__log_error(Error)

    def __log_error(self, error):
        self.__logger.warning("Failed to load plugin!")
        self.__logger.exception(error)

    def __add_option_module(self, module):
        self.__templates[module.request_metadata("name")] = \
            module.request_options("template")

    def __add_main_module(self, module):
        self.__templates[module.request_metadata("id")] = \
            module.request_options("template")

    @property
    def templates(self):
        return self.__templates