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

import io
import logging

import ruamel.yaml
import ruamel.yaml.parser

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ConfigParser(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    def read_config(self, configuration):
        """
        Parses the configuration that the user specified.

        Args:
            configuration (str): The name of the configuration file.

        Returns:
            dict: The configuration of the program.
        """
        # Using the word 'unclean' is hip, right?
        return self._parse_config(configuration)

    def _parse_config(self, configuration):
        """
        Reads in the configuration file into memory then returns the
        unfiltered dictionary.
            If there is a syntax error it will catch the error then raise
        a cleaned version of the error to not flood the user with
        unneeded information.
            The full exception will be passed to the logger if the user
        wants to see the full error, should only show if they have
        verboseness enabled.

        Args:
            configuration (str): The name of the configuration file.

        Returns:
            dict: The unfiltered dictionary of the configuration.

        Raises:
            SyntaxError: If there is a typo or other similar error in the
                configuration file.
        """
        with io.open(configuration, "r") as stream:
            try:
                return ruamel.yaml.load(
                    stream, ruamel.yaml.RoundTripLoader
                )
            except ruamel.yaml.parser.ParserError as UserError:
                self._logger.exception(UserError)
                raise SyntaxError(str(UserError))
