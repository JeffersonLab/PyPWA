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
import PyPWA.shell
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.configurator import _settings_aid
from PyPWA.configurator import config_loader
from PyPWA.core_libs import plugin_loader
from PyPWA.core_libs.templates import configurator_templates
from PyPWA.core_libs.templates import option_templates

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


class Configurator(configurator_templates.ShellCoreTemplate):

    def __init__(self):
        self._config_parser = config_loader.ConfigParser()
        self._settings_aid = _settings_aid.SettingsAid()

    def make_config(self, application_settings):
        """

        Args:
            application_settings (dict):
        """

    def run(self, function_settings, configuration_location):
        """

        Args:
            function_settings (dict):
            configuration_location:

        Returns:

        """
        extra_plugins = ""

        parsed_config = self._config_parser.read_config(
            configuration_location
        )

        for key in list(function_settings["main options"].keys()):
            parsed_config[function_settings["main name"]][key] = \
                function_settings["main options"][key]

        parsed_config[function_settings["main"]] = \
            parsed_config[function_settings["main name"]]

        parsed_config.pop(function_settings["main name"])

        try:
            extra_plugins = \
                parsed_config["Global Options"]["plugin directory"]
        except KeyError:
            pass

        storage = PluginStorage(extra_plugins)
        plugins_template = storage.templates_config

        complete_templates = \
            self._add_configuration_settings(plugins_template)

        correct_settings = self._settings_aid.correct_settings(
            parsed_config, complete_templates
        )

        launcher = ShellLauncher(storage, correct_settings)
        launcher.start()

    @staticmethod
    def _add_configuration_settings(templates):
        special_sauce = ConfiguratorOptions()
        templates[special_sauce.request_metadata("name")] = \
            special_sauce.request_options("templates")
        return templates


class ShellLauncher(object):

    def __init__(self, plugin_storage, settings):
        """

        Args:
            plugin_storage (PluginStorage):
            settings (dict):
        """
        self._plugin_storage = plugin_storage
        self._settings = settings

    def start(self):
        the_ids = list(self._settings.keys())
        main = None  # type: option_templates.MainOptionsTemplate
        plugins = {}
        initialized_plugins = {}

        for the_id in the_ids:
            temp = self._plugin_storage.request_plugin_by_name(the_id)
            if temp:
                plugins[the_id] = temp

        for the_id in the_ids:
            temp = self._plugin_storage.request_main_by_id(the_id)
            if temp:
                main = temp

        for plugin in plugins:
            name = plugin.request_metadata("name")
            the_type = plugin.request_metadata("provides")
            interface = plugin.request_metadata("interface")
            initialized = interface(self._settings[name])
            initialized_plugins[the_type] = initialized

        main_settings = self._settings[main.request_metadata("name")]

        for key in list(initialized_plugins.keys()):
            main_settings[key] = plugins[key]

        shell = main.request_metadata("object")
        initialized_shell = shell(main_settings)
        initialized_shell.start()


class PluginStorage(object):

    def __init__(self, extra_locations=None):
        plugins = [PyPWA.libs, PyPWA.shell]

        if isinstance(extra_locations, str):
            plugins.append(extra_locations)
        elif isinstance(extra_locations, list):
            for plugin in extra_locations:
                plugins.append(plugin)

        options_loader = plugin_loader.PluginLoading(
            option_templates.PluginsOptionsTemplate
        )

        shell_loader = plugin_loader.PluginLoading(
            option_templates.MainOptionsTemplate
        )

        self._plugins = options_loader.fetch_plugin(plugins)
        self._shell = shell_loader.fetch_plugin(plugins)

        templates = {}
        for plugin in self._plugins:
            templates[plugin.request_metadata("name")] = \
                plugin.request_options("template")

        for main in self._shell:
            templates[main.request_metadata("id")] = \
                main.request_options("template")

        self._templates = templates

    def request_main_by_id(self, the_id):
        """

        Args:
            the_id (str):

        Returns:

        """
        for main in self._shell:
            if main.request_metadata("id") == the_id:
                return main
        return False

    def request_plugin_by_name(self, name):
        for plugin in self._plugins:
            if plugin.request_metadata("name") == name:
                return plugin
        return False

    @property
    def templates_config(self):
        return self._templates


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


class ConfiguratorOptions(option_templates.PluginsOptionsTemplate):

    def _plugin_name(self):
        return "Global Options"

    def _plugin_interface(self):
        return False

    def _plugin_type(self):
        return False

    def _user_defined_function(self):
        return None

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
