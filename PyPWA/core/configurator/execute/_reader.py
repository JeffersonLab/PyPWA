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
Loads in the users configuration files.
---------------------------------------
- _ReadData - Abstract class used to define the config parsers
- _ReadYml - Loads the Yaml configuration files.
- _ReadJson - Loads the Json configuration files.
- ConfigurationLoader - Main object to call for loading configuration,
  defaults to Yml unless files extension is json.
"""

import json
import logging
import os
import io

from typing import Any, Dict

import ruamel.yaml

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _ReadData(object):

    __LOGGER = logging.getLogger(__name__ + "._ReadData")

    def read(self, configuration):
        # type: (str) -> Dict[str, Any]
        with io.open(configuration, "r") as stream:
            data = self._process_stream(stream)
            self.__LOGGER.info("Parsed %s" % configuration)
            return data

    def _process_stream(self, stream):
        # type: (io.TextIOWrapper) -> Dict[str, Any]
        raise NotImplementedError

    def _process_error(self, user_error):
        # type: (Exception) -> None
        self.__LOGGER.exception(user_error)
        raise SyntaxError(str(user_error))


class _ReadYml(_ReadData):

    def _process_stream(self, stream):
        # type: (io.TextIOWrapper) -> Dict[str, Any]
        try:
            return self.__load_configuration(stream)
        except ruamel.yaml.parser.ParserError as UserError:
            self._process_error(UserError)

    @staticmethod
    def __load_configuration(stream):
        # type: (io.TextIOWrapper) -> Dict[str, Any]
        return ruamel.yaml.load(stream, ruamel.yaml.RoundTripLoader)


class _ReadJson(_ReadData):

    def _process_stream(self, stream):
        # type: (io.TextIOWrapper) -> Dict[str, Any]
        try:
            return self._load_configuration(stream)
        except json.JSONDecodeError as UserError:
            self._process_error(UserError)

    @staticmethod
    def _load_configuration(stream):
        # type: (io.TextIOWrapper) -> Dict[str, Any]
        return json.loads(stream)


class ConfigurationLoader(object):

    __LOGGER = logging.getLogger(__name__ + ".ConfigurationLoader")

    def __init__(self):
        self.__json = _ReadJson()
        self.__yml = _ReadYml()

    def read_config(self, configuration):
        # type: (str) -> Dict[str, Any]
        if os.path.splitext(configuration)[1] is json:
            return self.__json.read(configuration)
        else:
            return self.__yml.read(configuration)
