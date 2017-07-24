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

import logging
from typing import Optional as Opt

from PyPWA import AUTHOR, VERSION
from PyPWA.libs import plugin_loader
from PyPWA.progs.shell import shell_types

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _ProcessFunctionLoader(object):

    __LOGGER = logging.getLogger(__name__ + "._ProcessingLoader")

    def __init__(self, loader, name):
        # type: (plugin_loader.PluginLoader, str) -> None
        self.__loader = loader
        self.__process_name = name
        self.__function = None  # type: shell_types.users_processing
        self.__try_to_load_processing_function()

    def __try_to_load_processing_function(self):
        try:
            self.__load_processing_function()
        except Exception as error:
            self.__handle_processing_error(error)

    def __load_processing_function(self):
        self.__function = self.__loader.get_by_name(self.__process_name)

    def __handle_processing_error(self, error):
        self.__LOGGER.critical("Failed to load %s!" % self.__process_name)
        raise error

    @property
    def process(self):
        # type: () -> shell_types.users_processing
        return self.__function


class _SetupFunctionLoader(object):

    __LOGGER = logging.getLogger(__name__ + "._SetupFunctionLoader")

    def __init__(self, loader, name):
        # type: (plugin_loader.PluginLoader, str) -> None
        self.__loader = loader
        self.__function = None  # type: shell_types.users_setup
        self.__process_setup_name(name)

    def __process_setup_name(self, name):
        # type: (Opt[str]) -> None
        if isinstance(name, str):
            self.__try_to_load_setup_function(name)
        else:
            self.__set_setup_to_empty()

    def __try_to_load_setup_function(self, name):
        # type: (str) -> None
        try:
            self.__load_setup_function(name)
        except Exception as error:
            self.__handle_setup_error(name, error)

    def __load_setup_function(self, name):
        # type: (str) -> None
        self.__function = self.__loader.get_by_name(name)

    def __handle_setup_error(self, name, error):
        # type: (str, Exception) -> None
        self.__LOGGER.critical("%s failed to load!" % name)
        self.__LOGGER.exception(error)
        self.__set_setup_to_empty()

    def __set_setup_to_empty(self):
        self.__LOGGER.info("No setup function found, settings to empty.")
        self.__function = self.__empty_function

    @staticmethod
    def __empty_function():
        # type: () -> None
        pass

    @property
    def setup(self):
        # type: () -> shell_types.users_setup
        return self.__function


class FunctionLoader(object):

    __LOGGER = logging.getLogger(__name__ + ".FunctionLoader")

    def __init__(self, location, process_name, setup_name=None):
        # type: (str, str, Opt[str]) -> None
        loader = plugin_loader.PluginLoader()
        loader.add_plugin_location(location)
        self.__process_loader = _ProcessFunctionLoader(loader, process_name)
        self.__setup_loader = _SetupFunctionLoader(loader, setup_name)

    @property
    def process(self):
        # type: () -> shell_types.users_processing
        return self.__process_loader.process

    @property
    def setup(self):
        # type: () -> shell_types.users_setup
        return self.__setup_loader.setup
