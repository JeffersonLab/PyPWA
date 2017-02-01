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


class ModuleStorage(object):

    _plugin_locations = [PyPWA.builtin_plugins, PyPWA.shell]
    _plugins = None  # type: list
    _shell = None  # type: list

    def __init__(self, extra_locations=False):
        if extra_locations:
            self._process_extra_functions(extra_locations)
        self._set_plugins()
        self._set_shell()

    def _process_extra_functions(self, locations):
        if isinstance(locations, str):
            self._plugin_locations.append(locations)
        elif isinstance(locations, type(PyPWA)):
            self._plugin_locations.append(locations)
        elif isinstance(locations, list):
            for location in locations:
                self._process_extra_functions(location)

    def _set_plugins(self):
        option_loader = plugin_loader.PluginLoading(
            option_templates.PluginsOptionsTemplate
        )

        self._plugins = option_loader.fetch_plugin(self._plugin_locations)

    def _set_shell(self):
        shell_loader = plugin_loader.PluginLoading(
            option_templates.MainOptionsTemplate
        )

        self._shell = shell_loader.fetch_plugin(self._plugin_locations)

    @property
    def shell_modules(self):
        return self._shell

    @property
    def option_modules(self):
        return self._plugins


class ModulePicking(object):

    _logger = logging.getLogger(__name__)
    _plugin_storage = None  # type: ModuleStorage

    def __init__(self, extra_locations=None):
        self._logger.addHandler(logging.NullHandler())
        self._plugin_storage = ModuleStorage(extra_locations)

    def request_main_by_id(self, the_id):
        for main in self._plugin_storage.shell_modules:
            the_main = self._safely_load_module(main)
            if not isinstance(the_main, type(None)):
                if the_main.request_metadata("id") == the_id:
                    return the_main

    def request_plugin_by_name(self, name):
        for plugin in self._plugin_storage.option_modules:
            the_plugin = self._safely_load_module(plugin)
            if not isinstance(the_plugin, type(None)):
                if the_plugin.request_metadata("name") == name:
                    return the_plugin

    def _safely_load_module(self, module):
        try:
            return module()
        except Exception as Error:
            self._log_error(Error)

    def _log_error(self, error):
        self._logger.error("Failed to load module!")
        self._logger.exception(error)


class ModuleTemplates(object):

    _logger = logging.getLogger(__name__)
    _plugin_storage = None  # type: ModuleStorage
    _templates = None  # type: dict

    def __init__(self, extra_locations=False):
        self._plugin_storage = ModuleStorage(extra_locations)
        self._logger.addHandler(logging.NullHandler())
        self._templates = {}
        self._process_options()
        self._process_main()

    def _process_options(self):
        for plugin in self._plugin_storage.option_modules:
            loaded = self._safely_load_module(plugin)
            if not isinstance(loaded, type(None)):
                self._add_option_module(loaded)

    def _process_main(self):
        for main in self._plugin_storage.shell_modules:
            loaded = self._safely_load_module(main)
            if not isinstance(loaded, type(None)):
                self._add_main_module(loaded)

    def _safely_load_module(self, module):
        try:
            return module()
        except Exception as Error:
            self._log_error(Error)

    def _log_error(self, error):
        self._logger.warning("Failed to load plugin!")
        self._logger.exception(error)

    def _add_option_module(self, module):
        self._templates[module.request_metadata("name")] = \
            module.request_options("template")

    def _add_main_module(self, module):
        self._templates[module.request_metadata("id")] = \
            module.request_options("template")

    @property
    def templates(self):
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
