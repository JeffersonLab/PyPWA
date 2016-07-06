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
__credits__ = ["Mark Jones", "Markus Jarderot @ Stack Overflow"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ConfigReader(object):

    def __init__(self, stream):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        self._stream = stream

    def read_config(self, configuration):
        """
        Parses the configuration that the user specified.

        Args:
            configuration (str): The name of the configuration file.

        Returns:
            dict: The configuration of the program.
        """
        # Using the word 'unclean' is hip, right?
        unclean_configuration = self._parse_config(configuration)
        return self._sanitize_keys(unclean_configuration)

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

    def _sanitize_keys(self, obj):
        """
        Cleans the keys of the loaded configuration. Should lowercase
        all keys no matter how many dictionaries are nested into the
        configuration.

        Args:
            obj (dict | list | str): The object that needs the keys of
                the dictionaries to be lower cased.

        Returns:
            dict: The object with the keys lower cased.

        See Also:
            http://stackoverflow.com/a/823072
        """
        if hasattr(obj, 'iteritems'):
            # A dictionary like object.
            new_dictionary = {}
            for key, value in obj.items():
                new_dictionary[key.lower()] = self._sanitize_keys(value)
            return new_dictionary
        elif hasattr(obj, '__iter__'):
            # An object that is list like.
            new_list = []
            for item in obj:
                new_list.append(self._sanitize_keys(item))
            return new_list
        else:
            return obj
