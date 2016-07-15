
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

import os
import logging
import pkgutil
import importlib
import sys

import ruamel.yaml.comments

from PyPWA.configurator import config_loader
import PyPWA.libs
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = [
    "Mark Jones",
    "jp. @ Stack Overflow",
    "unutbu @ Stack Overflow"
]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Configurator(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    def build(self, default_config, config_file):
        reader = config_loader.ConfigReader()
        configuration = reader.read_config(config_file)


class PluginLoading(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    @staticmethod
    def _list_modules(module):
        """
        Simple little function that

        Args:
            module (module): The unknown module that was loaded.

        Returns:
            list[str]: A list of all the modules found in the package.

        See Also:
            http://stackoverflow.com/a/1310912
            http://stackoverflow.com/a/1708706
        """
        # Should make a list of:
        # [ ImporterInstance, name of module, is a package ]
        names = [name for name in pkgutil.iter_modules(module.__path__)]
        # Credit to unutbu and jp. for the discovery of how pkgutil works.
        return names[1]

    @staticmethod
    def _import_lib(module_name):
        return importlib.import_module(module_name)

    def _find_libs(self, module):
        libs = []
        for module_name in self._list_modules(module):
            libs.append(
                importlib.import_module(
                    module.__name__ + "." + module_name
                )
            )
        return libs

    @staticmethod
    def _extract_metadata(plugins):
        plugin_metadata = []
        for plugin in plugins:
            try:
                for metadata in plugin.metadata:
                    plugin_metadata.append(metadata)
            except AttributeError:
                pass

        return plugin_metadata

    def load_plugin(self, plugin_list):
        for plugin in plugin_list:
            # Appends the directory containing the
            sys.path.append(os.path.dirname(os.path.abspath(plugin)))
            module = self._import_lib(
                # Extracts the filename from the path provided
                os.path.splitext(os.path.basename(plugin))[0]
            )

            libraries = self._find_libs(module)
#            if not libraries:


class MetadataStorage(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._minimization = {}
        self._kernel_processing = {}
        self._data = {}
        self._main = {}


    def add_plugins(self, plugins):
        for plugin in plugins:
            self._plugin_filter(plugin)

    def _plugin_filter(self, plugin):
        if plugin["provides"] == "data":
            self._data.update(plugin)
        elif plugin["provides"] == "minimization":
            self._minimization.update(plugin)
        elif plugin["provides"] == "kernel processing":
            self._kernel_processing.update(plugin)
        elif plugin["provides"] == "main":
            self._main.update(plugin)

    def search_plugin(self, plugin_name, plugin_type):
        if plugin_type is "data":
            return self._plugin_name_search(
                plugin_name, self._data
            )

        elif plugin_type is "minimization":
            return self._plugin_name_search(
                plugin_name, self._minimization
            )

        elif plugin_type is "kernel processing":
            return self._plugin_name_search(
                plugin_name, self._kernel_processing
            )

        elif plugin_type is "main":
            return self._plugin_name_search(
                plugin_name, self._main
            )

    @staticmethod
    def _plugin_name_search(plugin_name, plugins):
        for plugin in plugins:
            if plugin["name"] == plugin_name:
                return plugin
        else:
            raise ImportError(
                "Failed to find plugin {0}".format(plugin_name)
            )

    @property
    def minimization(self):
        return self._minimization

    @property
    def main(self):
        return self._main

    @property
    def kernel_processing(self):
        return self._kernel_processing

    @property
    def data(self):
        return self._data


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
