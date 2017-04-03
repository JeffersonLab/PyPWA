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
This loads all the plugins, then parses their templates into one massive
template dictionary.
"""

import logging

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator.storage import core_storage

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class TemplateLoader(object):

    __logger = logging.getLogger(__name__ + ".ModuleTemplates")
    __plugin_storage = None  # type: core_storage.ModuleStorage
    __templates = None  # type: dict

    def __init__(self, extra_locations=False):
        self.__plugin_storage = core_storage.ModuleStorage(extra_locations)
        self.__logger.addHandler(logging.NullHandler())
        self.__templates = {}
        self.__process_options()
        self.__process_main()

    def __process_options(self):
        for plugin in self.__plugin_storage.option_modules:
            self.__load_templates(plugin)

    def __process_main(self):
        for main in self.__plugin_storage.shell_modules:
            self.__load_templates(main)

    def __load_templates(self, plugin):
        loaded = self.__safely_load_module(plugin)
        if not isinstance(loaded, type(None)):
            self.__add_module(loaded)

    def __safely_load_module(self, module):
        try:
            return module()
        except Exception as Error:
            self.__log_error(Error)

    def __log_error(self, error):
        self.__logger.warning("Failed to load plugin!")
        self.__logger.exception(error)

    def __add_module(self, module):
        self.__templates[module.plugin_name] = module.option_types

    @property
    def templates(self):
        return self.__templates
