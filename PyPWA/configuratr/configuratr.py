# The MIT License (MIT)
#
# Copyright (c) 2014-2016 JLab.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
