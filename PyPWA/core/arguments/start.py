#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016 JLab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
The Argument Parser
-------------------
This is a simple utility that allows for simple programs to exist that only
have a few different options without needing to rely on a configuration file
to operate, while still using the same underlying plugin architecture, albeit
to a lesser extent.

- _PluginLoader - Loads the needed main and children plugins that are needed
  for the program.
- _LoadArguments - Takes the loaded plugins and creates a parser with all
  their options loaded into it.
- _SetupPlugins - This loads the plugins interfaces into a setup object and
  passes them to the main plugin.
- StartArguments - This is the main interface for the arguments in the
  package. This walks takes the initial data provided and loads the needed
  plugins and a argument parser to go with it, then launches the main plugin.
"""

import argparse
import sys
from typing import Dict, List

from PyPWA import AUTHOR, VERSION
from PyPWA.core.arguments import _loader
from PyPWA.core.arguments import arguments_options
from PyPWA.core.shared.interfaces import plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _PluginLoader(object):

    def __init__(self):
        self.__main = None  # type: arguments_options.Main
        self.__children = {}  # type: Dict[str, arguments_options.Plugin]
        self.__loader = _loader.RequestedFetcher()

    def load(self, name):
        # type: (str) -> None
        self.__load_main_plugin(name)
        self.__iterate_over_requested()

    def __load_main_plugin(self, name):
        # type: (str) -> None
        self.__main = self.__loader.get_plugin_by_name(name)

    def __iterate_over_requested(self):
        for requested in self.__main.get_required():
            self.__load_child_plugin(requested)

    def __load_child_plugin(self, name):
        # type: (str) -> None
        self.__children[name] = self.__loader.get_plugin_by_name(name)

    @property
    def plugins(self):
        # type: () -> Dict[str, arguments_options.Plugin]
        return self.__children

    @property
    def main(self):
        # type: () -> arguments_options.Main
        return self.__main


class _LoadArguments(object):

    def __init__(self):
        self.__arguments = sys.argv[1:]
        self.__root_parser = None  # type: argparse.ArgumentParser
        self.__plugins = None  # type: _PluginLoader
        self.__namespace = None  # type: argparse.Namespace

    def load_arguments(self, plugin_storage, description):
        # type: (_PluginLoader, str) -> None
        self.__plugins = plugin_storage
        self.__setup_root_parser(description)
        self.__load_main_arguments()
        self.__load_children_arguments()
        self.__parse_arguments()

    def __setup_root_parser(self, description):
        # type: (str) -> None
        self.__root_parser = argparse.ArgumentParser(description)

    def __load_main_arguments(self):
        self.__plugins.main.setup(self.__root_parser)

    def __load_children_arguments(self):
        for plugin in self.__plugins.plugins.values():
            plugin.setup(self.__root_parser)

    def __parse_arguments(self):
        # type: (List[str]) -> None
        self.__namespace = self.__root_parser.parse_args(self.__arguments)

    @property
    def namespace(self):
        return self.__namespace


class _SetupPlugins(object):

    def __init__(self):
        self.__plugins = None  # type: _PluginLoader
        self.__arguments = None  # type: _LoadArguments
        self.__child_interfaces = {}  # type: Dict[str, plugins.BasePlugin]
        self.__main_interface = None  # type: plugins.Main

    def create_main_program(self, plugin_storage, arguments):
        # type: (_PluginLoader, _LoadArguments) -> None
        self.__plugins = plugin_storage
        self.__arguments = arguments
        self.__iterate_over_children()
        self.__setup_main_plugin()

    def __iterate_over_children(self):
        for name, plugin in self.__plugins.plugins.items():
            self.__setup_child_plugin(name, plugin)

    def __setup_child_plugin(self, name, plugin):
        # type: (str, arguments_options.Plugin) -> None
        interface = plugin.get_interface(self.__arguments.namespace)
        self.__child_interfaces[name] = interface

    def __setup_main_plugin(self):
        self.__main_interface = self.__plugins.main.get_interface(
            self.__arguments.namespace, self.__child_interfaces
        )

    @property
    def main(self):
        # type: () -> plugins.Main
        return self.__main_interface


class StartArguments(object):

    def __init__(self):
        self.__plugins = _PluginLoader()
        self.__arguments = _LoadArguments()
        self.__setup = _SetupPlugins()

    def start(self, name, description):
        # type: (str, str) -> None
        self.__plugins.load(name)
        self.__arguments.load_arguments(self.__plugins, description)
        self.__setup.create_main_program(self.__plugins, self.__arguments)
        self.__setup.main.start()
