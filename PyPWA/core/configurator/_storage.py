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

import logging

import PyPWA.builtin_plugins
import PyPWA.shell
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core import plugin_loader
from PyPWA.core.templates import option_templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class PluginStorage(object):

    def __init__(self, extra_locations=None):
        plugins = [PyPWA.builtin_plugins, PyPWA.shell]

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
            the_plugin = plugin()
            templates[the_plugin.request_metadata("name")] = \
                the_plugin.request_options("template")

        for main in self._shell:
            the_main = main()
            templates[the_main.request_metadata("id")] = \
                the_main.request_options("template")

        self._templates = templates

    def request_main_by_id(self, the_id):
        for main in self._shell:
            the_main = main()
            if the_main.request_metadata("id") == the_id:
                return the_main
        return False

    def request_plugin_by_name(self, name):
        for plugin in self._plugins:
            the_plugin = plugin()
            if the_plugin.request_metadata("name") == name:
                return the_plugin
        return False

    @property
    def templates_config(self):
        return self._templates


class MetadataStorage(object):

    _logger = logging.getLogger(__name__)
    _actual_storage = None  # type: {}

    def __init__(self):
        self._logger.addHandler(logging.NullHandler())
        self._actual_storage = {}

    def add_plugins(self, plugins):
        for plugin in plugins:
            loaded_plugin = self._get_initialized_plugin(plugin)

            if not self._should_skip(loaded_plugin):
                self._add_type(loaded_plugin)
                self._plugin_filter(plugin, loaded_plugin)

    def _get_initialized_plugin(self, plugin):
        try:
            temp_object = plugin()
            return temp_object
        except Exception as Error:
            self._logger.error(Error)

    @staticmethod
    def _should_skip(plugin):
        if isinstance(plugin, type(None)):
            return True
        else:
            return False

    def _add_type(self, plugin):
        plugin_type = self._get_plugin_type(plugin)
        if not self._plugin_type_included(plugin_type):
            self._actual_storage[plugin_type] = []

    @staticmethod
    def _get_plugin_type(plugin):
        return plugin.request_metadata("provides")

    def _plugin_type_included(self, plugin_type):
        if plugin_type in self._actual_storage.keys():
            return True
        else:
            return False

    def _plugin_filter(self, plugin, loaded_plugin):
        plugin_type = self._get_plugin_type(loaded_plugin)
        self._actual_storage[plugin_type].append(plugin)

    def search_plugin(self, plugin_name, plugin_type):
        if self._plugin_type_included(plugin_type):
            return self._plugin_name_search(plugin_name, plugin_type)
        else:
            self._cant_find_plugin(plugin_name)

    def _plugin_name_search(self, plugin_name, plugin_type):
        for plugin in self._actual_storage[plugin_type]:
            name = self._get_plugin_name(plugin)
            if name == plugin_name:
                return plugin
        else:
            self._cant_find_plugin(plugin_name)

    def _get_plugin_name(self, plugin):
        loaded_plugin = self._get_initialized_plugin(plugin)
        return loaded_plugin.request_metadata("name")

    def _cant_find_plugin(self, plugin_name):
        error = "Failed to find plugin {0}".format(plugin_name)
        self._logger.error(error)
        raise ImportError(error)

    def request_plugin_by_type(self, plugin_type):
        if self._plugin_type_included(plugin_type):
            return self._actual_storage[plugin_type]

    def return_plugin_types(self):
        return self._actual_storage.keys()
