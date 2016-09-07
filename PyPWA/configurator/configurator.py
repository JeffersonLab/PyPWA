
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

import PyPWA.libs
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core_libs import templates, plugin_loader

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


class Configurator(templates.ShellCoreTemplate):

    def __init__(self):
        self._loader = plugin_loader.PluginLoading(
            templates.OptionsTemplate
        )

        builtins = self._loader.fetch_plugin([PyPWA.libs])

        self._storage = MetadataStorage()
        self._storage.add_plugins(builtins)

    def make_config(self, application_settings):
        """

        Args:
            application_settings (dict):
        """

    def run(self, application_settings):
        """

        Args:
            application_settings (dict):
        """




class MetadataStorage(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._minimization = []
        self._kernel_processing = []
        self._data_reader = []
        self._data_parser = []
        self._main = []

    def add_plugins(self, plugins):
        for plugin in plugins:
            self._plugin_filter(plugin)

    def _plugin_filter(self, plugin):
        try:
            temp_object = plugin()
            plugin_type = temp_object.request_metadata("provides")

            if plugin_type == "data reader":
                self._data_reader.append(plugin)
            elif plugin_type == "data parser":
                self._data_parser.append(plugin)
            elif plugin_type == "minimization":
                self._minimization.append(plugin)
            elif plugin_type == "kernel processing":
                self._kernel_processing.append(plugin)
            elif plugin_type == "main":
                self._main.append(plugin)

        except Exception as Error:
            self._logger.error(Error)

    def search_plugin(self, plugin_name, plugin_type):
        if plugin_type is "data reader":
            return self._plugin_name_search(
                plugin_name, self._data_reader
            )

        elif plugin_type is "data parser":
            return self._plugin_name_search(
                plugin_name, self._data_parser
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
    def data_reader(self):
        return self._data_reader

    @property
    def data_parser(self):
        return self._data_parser


class ConfiguratorOptions(templates.OptionsTemplate):

    def _plugin_name(self):
        return "Global Options"

    def _plugin_interface(self):
        return False

    def _plugin_type(self):
        return False

    def _plugin_arguments(self):
        return False

    def _plugin_requires(self):
        return False

    def _default_options(self):
        return {
            "plugin directory": "none",
            "logging": [
                "debug", "info", "warning",
                "error", "critical", "fatal"
            ]
        }

    def _option_levels(self):
        return {
            "plugin directory": self._advanced,
            "logging": self._optional
        }

    def _option_types(self):
        return {
            "plugin directory": str,
            "logging": [
                "debug", "info", "warning",
                "error", "critical", "fatal"
            ]
        }

    def _option_comments(self):
        return {
            "plugin directory":
                "This is the option that you would add your own plugins "
                "to the system. Supported plugins are Data parsing and "
                "writing, minimization, and even new programs "
                "capitalizing on the internal frameworking of "
                "the program.",
            "logging":
                "This sets the logging level of the program, supported "
                "options are debug, info, warning, error, critical, and "
                "fatal. This setting will be overwritten by the command "
                "prompt if the user specifies -v"
        }

    def _main_comment(self):
        return "This is the global loaders settings. These settings " \
               "are the options that will be set for the entire program."
