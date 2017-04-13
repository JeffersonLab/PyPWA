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
Simply loads the configuration file using ruamel.yaml.
"""

import logging

import ruamel.yaml
import ruamel.yaml.comments
import ruamel.yaml.parser

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ConfigurationLoader(object):

    __logger = logging.getLogger(__name__ + ".ConfigurationLoader")

    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())

    def read_config(self, configuration):
        with open(configuration, "r") as stream:
            return self.__process_stream(stream)

    def __process_stream(self, stream):
        try:
            return self.__load_configuration(stream)
        except ruamel.yaml.parser.ParserError as UserError:
            self.__process_error(UserError)

    @staticmethod
    def __load_configuration(stream):
        return ruamel.yaml.load(stream, ruamel.yaml.RoundTripLoader)

    def __process_error(self, user_error):
        self.__logger.exception(user_error)
        raise SyntaxError(str(user_error))
