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

"""The utility objects for the Data Plugin

This holds all the main objects for the data plugin. This has search functions
but these objects should never know anything about the data plugin they are
trying to load, all it should ever care about is that there is metadata that
contains enough information about the plugin for this to get started passing
data to it.
"""

import logging

import ruamel.yaml
import ruamel.yaml.comments

from PyPWA.configuratr import tools
from PyPWA.libs.data import definitions
from PyPWA.libs.data import _utilites
from PyPWA.libs.data import builtin
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION

BUILTIN_PACKAGE_LOCATION = builtin


class Options(object):
    _options = {  # Holds the default options for the builtin.
        "cache": True,  # Optional
        "clear cache": False,  # Advanced
        "fail": False,  # Advanced
        "user plugin": "cwd=/path/to/file;"  # Advanced
    }

    _template = {  # Holds the actual expected options and names for the builtin
        "cache": bool,
        "clear cache": bool,
        "fail": bool,
        "user plugin": str
    }

    def __init__(self):
        """
        Option object for the Data Builtin Plugin.
        """
        header = self._build_empty_options_with_comments()
        self._optional = self._build_optional(header)
        self._advanced = self._build_advanced(header)
        self._required = ruamel.yaml.comments.CommentedMap()

    @staticmethod
    def _build_empty_options_with_comments():
        """
        Builds an empty dictionary with all the comments for the builtin
        data dictionary.

        Returns:
            ruamel.yaml.comments.CommentedMap: The empty dictionary with the
                comments.
        """
        header = ruamel.yaml.comments.CommentedMap()
        content = ruamel.yaml.comments.CommentedMap()

        header[_utilites.MODULE_NAME] = content
        header.yaml_add_eol_comment('This is the builtin data parser, you can '
                                    'replace this with your own data parser if '
                                    'you wish.', _utilites.MODULE_NAME)

        content.yaml_add_eol_comment("Should Cache be enabled? The cache will"
                                     "automatically clear if it detects a"
                                     "change in any of your data and should be"
                                     "safe to leave enabled.", "cache")
        content.yaml_add_eol_comment("Should we force the cache to clear? This"
                                     "will destroy all of your caches, this"
                                     "means loading your data will take much"
                                     "longer, its recommended to leave this off"
                                     "unless you are certain its a cache "
                                     "issue.", "clear cache")
        content.yaml_add_eol_comment("Should the program stop if it fails to "
                                     "load the file? The program will already"
                                     "fail if the data is needed for parsing"
                                     "to happen, if this is set to true even"
                                     "files that are optional will cause the "
                                     "program to stop.", "fail")
        content.yaml_add_eol_comment("A plugin that can be loaded into the "
                                     "the " + _utilites.MODULE_NAME + " for "
                                     "parsing, see the documentation on the " +
                                     _utilites.MODULE_NAME + " plugin for more "
                                     "information.", "user plugin")
        return header

    def _build_optional(self, header):
        """
        Loads the optional data into the dictionary.

        Args:
            header (ruamel.yaml.comment.CommentedMap): The dictionary with the
                pre-nested comments.

        Returns:
            ruamel.yaml.comment.CommentedMap: The dictionary with the optional
                options.
        """
        header[_utilites.MODULE_NAME]["cache"] = self._options["cache"]
        return header

    def _build_advanced(self, header):
        """
        Loads the optional and advanced data into the dictionary.

        Args:
            header (ruamel.yaml.comment.CommentedMap): The dictionary with the
             pre-nested comments.

        Returns:
            ruamel.yaml.comment.CommentedMap: The dictionary with the optional
                and advanced options.
        """
        header = self._build_optional(header)
        header[_utilites.MODULE_NAME]["clear cache"] = \
            self._options["clear cache"]

        header[_utilites.MODULE_NAME]["fail"] = self._options["fail"]
        return header

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

    @property
    def return_defaults(self):
        return self._options


class _DataInterface(object):

    def __init__(self):
        self._is_ready = False
        self._data_type = None  # type: str

    @property
    def is_ready(self):
        return self._is_ready

    @property
    def wait(self):
        raise NotImplementedError(str(self.__class__.__name__) + " does not "
                                  "implement the wait property")


class TrafficCop(object):

    def __init__(self, settings):
        fixer = tools.CorrectSettings()
        options = Options()
        corrected_settings = fixer.correct_dictionary(settings,
                                                      options.return_template)


        if isinstance(external_packages, str):
            packages = [external_packages, BUILTIN_PACKAGE_LOCATION]
        elif isinstance(external_packages, list):
            packages = external_packages + [BUILTIN_PACKAGE_LOCATION]
        else:
            packages = [BUILTIN_PACKAGE_LOCATION]

        plugins = self._index_packages(packages)
        self._search = _utilites.DataSearch(plugins)

        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    @staticmethod
    def _index_packages(packages):
        plugins = []
        loader = _utilites.FindPlugins()
        for package in packages:
            plugins.append(loader.find_plugin(package))

        return plugins


