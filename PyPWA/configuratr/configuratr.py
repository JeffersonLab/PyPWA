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

"""
This file is the main file for all of PyPWA. This file takes a
configuration file, processes it, then contacts the main module that is
requested to determine what information is needed to be loaded and how it needs
to be structured to be able to function in the users desired way.
"""

import logging

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class DataConfiguratr(object):
    def __init__(self, data):
        """
        This object stores the configuration data for the data in a way that can
        be applied for all configuration throughout the program. This could
        probably be made in a different way that would be more efficient, ie
        tuples, but this does the job for now and ultimately shouldn't be
        initialized more than a few times throughout the existence of a single
        operation.

        Args:
            data (dict) : The dictionary containing the configuration loaded
                from file.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler)
        self._parse_data(data)
        self._save_location = False
        self._accepted_location = False
        self._data_location = False
        self._qfactor_location = False

    def _parse_data(self, data):
        # This lower cases just the keys in the dictionary.
        new_data = {k.lower(): v for k, v in data.items()}
        if "save name" in new_data:
            self._parse_save_location(new_data["save name"])

        if "data location" in new_data:
            self._parse_data_location(new_data["data location"])

        if "accepted monte carlo location" in new_data:
            self._parse_accepted_location(
                new_data["accepted monte carlo location"])

        if "qfactor list location" in new_data:
            self._parse_qfactor_location(new_data["qfactor list location"])

    def _parse_save_location(self, data):
        if isinstance(data, str) or isinstance(data, list):
            self._save_location = data
        else:
            self.logger.warning("Expected \"Save Name\" to be string or list, "
                                "but found {0} instead!".format(type(data)))

    def _parse_data_location(self, data):
        if isinstance(data, str):
            self._data_location = data
        else:
            self.logger.warning("Expected \"Data Location\" to be a string, but"
                                " found {0} instead!".format(type(data)))

    def _parse_accepted_location(self, data):
        if isinstance(data, str):
            self._accepted_location = data
        else:
            self.logger.warning("Expected \"Accepted Monte Carlo Location\" to "
                                "be a string, but found {0} "
                                "instead!".format(type(data)))

    def _parse_qfactor_location(self, data):
        if isinstance(data, str):
            self._qfactor_location = data
        else:
            self.logger.warning("Expected \"QFactor List Location\" to be a "
                                "string, but found {0} "
                                "instead!".format(type(data)))

    @property
    def save_location(self):
        return self._save_location

    @property
    def qfactor_location(self):
        return self._qfactor_location

    @property
    def monte_carlo_location(self):
        return self._accepted_location

    @property
    def data_location(self):
        return self._data_location
