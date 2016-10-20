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

"""

import logging

import PyPWA.libs
import PyPWA.shell
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core_libs import plugin_loader
from PyPWA.core_libs.templates import option_templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class PluginStorage(object):

    def __init__(self, extra_locations=None):
        """

        Args:
            extra_locations:
        """
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
            the_plugin = plugin()
            templates[the_plugin.request_metadata("name")] = \
                the_plugin.request_options("template")

        for main in self._shell:
            the_main = main()
            templates[the_main.request_metadata("id")] = \
                the_main.request_options("template")

        self._templates = templates

    def request_main_by_id(self, the_id):
        """

        Args:
            the_id (str):

        Returns:

        """
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

    def __init__(self):
        """

        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._minimization = []
        self._kernel_processing = []
        self._data_reader = []
        self._data_parser = []

    def add_plugins(self, plugins):
        """

        Args:
            plugins:

        Returns:

        """
        for plugin in plugins:
            self._plugin_filter(plugin)

    def _plugin_filter(self, plugin):
        """

        Args:
            plugin:

        Returns:

        """
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

        except Exception as Error:
            self._logger.error(Error)

    def search_plugin(self, plugin_name, plugin_type):
        """

        Args:
            plugin_name:
            plugin_type:

        Returns:

        """
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

    @staticmethod
    def _plugin_name_search(plugin_name, plugins):
        """

        Args:
            plugin_name:
            plugins:

        Returns:

        """
        for plugin in plugins:
            if plugin["name"] == plugin_name:
                return plugin
        else:
            raise ImportError(
                "Failed to find plugin {0}".format(plugin_name)
            )

    @property
    def minimization(self):
        """

        Returns:

        """
        return self._minimization

    @property
    def kernel_processing(self):
        """

        Returns:

        """
        return self._kernel_processing

    @property
    def data_reader(self):
        """

        Returns:

        """
        return self._data_reader

    @property
    def data_parser(self):
        """

        Returns:

        """
        return self._data_parser
