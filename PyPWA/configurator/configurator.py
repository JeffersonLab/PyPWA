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

import PyPWA.libs
import PyPWA.shell
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.configurator import _storage
from PyPWA.configurator import _tools
from PyPWA.configurator import config_loader
from PyPWA.core_libs import plugin_loader
from PyPWA.core_libs.templates import configurator_templates
from PyPWA.core_libs.templates import option_templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Configurator(configurator_templates.ShellCoreTemplate):

    def __init__(self):
        self._config_parser = config_loader.ConfigParser()
        self._settings_aid = _tools.SettingsAid()

    def make_config(self, function_settings, application_settings):
        """

        Args:
            function_settings:
            application_settings:

        Returns:

        """
        main_plugin = None
        plugin_name = function_settings["main name"]
        plugin_id = function_settings["main"]
        settings = None

        try:
            settings = function_settings["main options"]
        except KeyError:
            pass

        loader = plugin_loader.PluginLoading(
            option_templates.MainOptionsTemplate
        )

        plugin_list = loader.fetch_plugin([PyPWA.shell])

        for plugin in plugin_list:
            temp_object = plugin()
            if temp_object.request_metadata("id") == plugin_id:
                main_plugin = temp_object
                break

        config_maker = config_loader.SimpleConfigBuilder()

        config_maker.build_configuration(
            plugin_name, main_plugin, settings,
            application_settings.configuration
        )

    def run(self, function_settings, configuration_location):
        """

        Args:
            function_settings (dict):
            configuration_location:

        Returns:

        """
        extra_plugins = False

        parsed_config = self._config_parser.read_config(
            configuration_location
        )

        try:
            for key in list(function_settings["main options"].keys()):
                parsed_config[function_settings["main name"]][key] = \
                    function_settings["main options"][key]
        except KeyError:
            pass

        parsed_config[function_settings["main"]] = \
            parsed_config[function_settings["main name"]]

        parsed_config.pop(function_settings["main name"])

        try:
            extra_plugins = \
                parsed_config["Global Options"]["plugin directory"]
        except KeyError:
            pass

        storage = _storage.PluginStorage(extra_plugins)
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
