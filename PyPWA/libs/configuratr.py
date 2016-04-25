"""
This file shall be majestic
"""

from PyPWA import VERSION, LICENSE, STATUS

import logging

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class DataConfiguratr(object):
    """Stores the parsed Data Configuration
    This object stores the configuration data for the data in a way
    that can be applied for all configuration throughout the program.
    This could probably be made in a different way that would be more
    efficient, ie tuples, but this does the job for now and ultimately
    shouldn't be initialized more than a few times throughout the
    existence of a single operation.

    Args:
        data (dict) : The dictionary containing the configuration loaded from file.
    """
    def __init__(self, data):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler)
        self._parse_data(data)
        self._save_location = False
        self._accepted_location = False
        self._data_location = False
        self._qfactor_location = False

    def _parse_data(self, data):
        new_data = {k.lower(): v for k, v in data.items()}  # This lower cases just the keys in the dictionary.
        if "save name" in new_data:
            self._parse_save_location(new_data["save name"])
        if "data location" in new_data:
            self._parse_data_location(new_data["data location"])
        if "accepted monte carlo location" in new_data:
            self._parse_accepted_location(new_data["accepted monte carlo location"])
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
            self.logger.warning("Expected \"Data Location\" to be a string, but found"
                                " {0} instead!".format(type(data)))

    def _parse_accepted_location(self, data):
        if isinstance(data, str):
            self._accepted_location = data
        else:
            self.logger.warning("Expected \"Accepted Monte Carlo Location\" to be a string, but found"
                                " {0} instead!".format(type(data)))

    def _parse_qfactor_location(self, data):
        if isinstance(data, str):
            self._qfactor_location = data
        else:
            self.logger.warning("Expected \"QFactor List Location\" to be a string, but found"
                                " {0} instead!".format(type(data)))

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


#class MinuitConfiguratr(object):
#    def __init__(self):