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

import ruamel.yaml
import ruamel.yaml.comments
import ruamel.yaml.parser

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ConfigurationLoader(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    def read_config(self, configuration):
        with open(configuration, "r") as stream:
            return self._process_stream(stream)

    def _process_stream(self, stream):
        try:
            return self._load_configuration(stream)
        except ruamel.yaml.parser.ParserError as UserError:
            self._process_error(UserError)

    @staticmethod
    def _load_configuration(stream):
        return ruamel.yaml.load(stream, ruamel.yaml.RoundTripLoader)

    def _process_error(self, user_error):
        self._logger.exception(user_error)
        raise SyntaxError(str(user_error))
