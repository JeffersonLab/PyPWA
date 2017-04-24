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

import json
import logging
import os

import ruamel.yaml

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _ReadData(object):
    __logger = logging.getLogger(__name__ + "._ReadData")

    def read(self, configuration):
        with open(configuration, "r") as stream:
            data = self._process_stream(stream)
            self.__logger.info("Parsed %s" % configuration)
            return data

    def _process_stream(self, stream):
        raise NotImplementedError

    def _process_error(self, user_error):
        self.__logger.exception(user_error)
        raise SyntaxError(str(user_error))


class _ReadYml(_ReadData):
    def _process_stream(self, stream):
        try:
            return self.__load_configuration(stream)
        except ruamel.yaml.parser.ParserError as UserError:
            self._process_error(UserError)

    @staticmethod
    def __load_configuration(stream):
        return ruamel.yaml.load(stream, ruamel.yaml.RoundTripLoader)


class _ReadJson(_ReadData):
    def _process_stream(self, stream):
        try:
            return self._load_configuration(stream)
        except json.JSONDecodeError as UserError:
            self._process_error(UserError)

    @staticmethod
    def _load_configuration(stream):
        return json.loads(stream)


class ConfigurationLoader(object):
    __logger = logging.getLogger(__name__ + ".ConfigurationLoader")
    __json = _ReadJson()
    __yml = _ReadYml()

    def read_config(self, configuration):
        if os.path.splitext(configuration)[1] is json:
            return self.__json.read(configuration)
        else:
            return self.__yml.read(configuration)
