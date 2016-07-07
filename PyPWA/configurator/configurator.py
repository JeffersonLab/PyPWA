
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
requested to determine what information is needed to be loaded and how it
needs to be structured to be able to function in the users desired way.
"""

import logging

import ruamel.yaml.comments

from PyPWA.libs import (process, data, minimizers)
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ConfigurationInitializer(object):
    pass


class Configurator(object):

    _builtin_libraries = [process, data, minimizers]

    def __init__(self, starter):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())


class ConfiguratorOptions(object):
    _options = {
        # Advanced
        "plugin directory": "./plugins/",
        # Optional
        "logging": "error"
    }

    _template = {
        "plugin directory": str,
        "logging": [
            "debug", "info", "warning",
            "error", "critical", "fatal"
        ]
    }

    def __init__(self):
        """
        Simple Object to hold the options for the Foreman.
        """
        header = self._build_empty_options_with_comments()
        self._optional = self._build_optional(header)
        self._advanced = self._build_advanced(header)
        self._required = header

    @staticmethod
    def _build_empty_options_with_comments():
        header = ruamel.yaml.comments.CommentedMap()
        content = ruamel.yaml.comments.CommentedMap()

        header["global"] = content
        header.yaml_add_eol_comment(
            "This is the global loaders settings. These settings are the "
            "options that will be set for the entire program.",
            "global"
        )

        content.yaml_add_eol_comment(
            "This is the option that you would add your own plugins to "
            "the system. Supported plugins are Data parsing and writing, "
            "minimization, and even new programs capitalizing on the "
            "internal frameworking of the program.",
            "plugin directory"
        )

        content.yaml_add_eol_comment(
            "This sets the logging level of the program, supported "
            "options are debug, info, warning, error, critical, and "
            "fatal. This setting will be overwritten by the command "
            "prompt if the user specifies -v",
            "logging"
        )

        return header

    def _build_optional(self, header):
        """
        Since there is only one option, and its optional, we only have a
        single building function for the actual options.

        Args:
            header (ruamel.yaml.comments.CommentedMap): The empty
                dictionary with the comments included.

        Returns:
            ruamel.yaml.comments.CommentedMap: The dictionary with the
                optional fields.
        """
        header["global"]["logging"] = self._options["logging"]
        return header

    def _build_advanced(self, header):
        options = self._build_optional(header)

        options["global"]["plugin directory"] = \
            self._options["plugin directory"]

        return options

    @property
    def return_template(self):
        return self._template

    @property
    def return_required(self):
        return self._required

    @property
    def return_optional(self):
        return self._optional

    @property
    def return_advanced(self):
        return self._advanced
