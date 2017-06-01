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
Handles all setting overrides
-----------------------------

- _ExternalizeName - Swaps the internal name for the shell plugin for the
  external name
  
- RemovePredefinedOptions - Takes any options that are defined in the entries
  and removes them from the configuration.
  
- Override - The main override object.
"""

import logging
from typing import Any, Dict

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _ExternalizeName(object):

    __LOGGER = logging.getLogger(__name__ + "._ExternalizeName")

    def __init__(self):
        self.__configuration = None  # type: Dict[str, Any]
        self.__internal_name = None  # type: str
        self.__external_name = None  # type: str

    def override(self, configuration, override):
        # type: (Dict[str, Any], Dict[str, Any]) -> None
        self.__set_configuration(configuration)
        self.__find_names(override)
        self.__externalize_shell_name()
        self.__remove_old_name()

    def __set_configuration(self, configuration):
        # type: (Dict[str, Any]) -> None
        self.__configuration = None
        self.__configuration = configuration

    def __find_names(self, override):
        # type: (Dict[str, Any]) -> None
        self.__internal_name = override["main"]
        self.__external_name = override["main name"]

    def __externalize_shell_name(self):
        self.__LOGGER.debug("Converting '%s'to '%s'" % (
            self.__internal_name, self.__external_name
        ))
        shell_options = self.__configuration[self.__internal_name]
        self.__configuration[self.__external_name] = shell_options

    def __remove_old_name(self):
        self.__configuration.pop(self.__internal_name)

    @property
    def configuration(self):
        # type: () -> Dict[str, Any]
        return self.__configuration


class _RemovePredefinedOptions(object):

    __LOGGER = logging.getLogger(__name__ + "._RemovePredefinedOptions")

    def __init__(self):
        self.__configuration = None  # type: Dict[str, Any]
        self.__predefined_options = None  # type: Dict[str, Any]
        self.__name = None  # type: str

    def override(self, configuration, override):
        # type: (Dict[str, Any], Dict[str, Any]) -> None
        self.__set_configuration(configuration)
        self.__setup_override(override)
        self.__process_options()

    def __set_configuration(self, configuration):
        # type: (Dict[str, Any]) -> None
        self.__configuration = configuration

    def __setup_override(self, override):
        # type: (Dict[str, Any]) -> None
        if "main options" in override:
            self.__LOGGER.debug("Removing override options.")
            self.__predefined_options = override["main options"]
            self.__name = override["main name"]
        else:
            self.__predefined_options = None
            self.__LOGGER.debug("No options to override.")

    def __process_options(self):
        if self.__predefined_options:
            self.__pop_unneeded_options()

    def __pop_unneeded_options(self):
        for option in self.__predefined_options:
            self.__LOGGER.debug("Removing option '%s'" % option)
            self.__configuration[self.__name].pop(option)

    @property
    def configuration(self):
        # type: () -> Dict[str, Any]
        return self.__configuration


class Override(object):

    def __init__(self):
        self.__externalize = _ExternalizeName()
        self.__predefined_options = _RemovePredefinedOptions()
        self.__override = None  # type: Dict[str, Any]
        self.__configuration = None # type: Dict[str, Any]

    def execute(self, configuration, override):
        # type: (Dict[str, Any], Dict[str, Any]) -> None
        self.__override = override
        self.__configuration = configuration
        self.__start_processing()

    def __start_processing(self):
        self.__externalize_shell_name()
        self.__remove_predefined_options()

    def __externalize_shell_name(self):
        self.__externalize.override(self.__configuration, self.__override)
        self.__configuration = self.__externalize.configuration

    def __remove_predefined_options(self):
        self.__predefined_options.override(
            self.__configuration, self.__override
        )
        self.__configuration = self.__predefined_options.configuration

    @property
    def processed_configuration(self):
        # type: () -> Dict[str, Any]
        return self.__configuration
