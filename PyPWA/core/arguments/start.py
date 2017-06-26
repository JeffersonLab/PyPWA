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
A simple blank module that exists purely for testing.
"""

import sys
import argparse
from typing import Dict
from PyPWA.core.arguments import _loader
from PyPWA.core.arguments import arguments_options
from PyPWA.core.shared.interfaces import plugins
from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _PluginStorage(object):

    def __init__(self):
        self.__main = None  # type: arguments_options.Main
        self.__children = {}  # type: Dict[arguments_options.Plugin]
        self.__loader = _loader.RequestedFetcher()

    def load(self, name):
        self.__load_main_plugin(name)
        self.__iterate_over_requested()

    def __load_main_plugin(self, name):
        self.__main = self.__loader.get_plugin_by_name(name)

    def __iterate_over_requested(self):
        for requested in self.__main.get_required():
            self.__load_child_plugin(requested)

    def __load_child_plugin(self, name):
        self.__children[name] = self.__loader.get_plugin_by_name(name)

    @property
    def plugins(self):
        return self.__children

    @property
    def main(self):
        return self.__main


class _ArgPrimer(object):

    def __init__(self):
        self.__root_parser = None  # type: argparse.ArgumentParser
        self.__plugins = None  # type: _PluginStorage
        self.__namespace = None  # type: argparse.Namespace

    def prime_plugins(self, plugins, description):
        # type: (_PluginStorage, str) -> None
        self.__plugins = plugins
        self.__setup_root_parser(description)
        self.__prime_main_plugin()
        self.__prime_children_plugins()
        self.__parse_arguments()

    def __setup_root_parser(self, description):
        self.__root_parser = argparse.ArgumentParser(description)

    def __prime_main_plugin(self):
        self.__plugins.main.setup(self.__root_parser)

    def __prime_children_plugins(self):
        for plugin in self.__plugins.plugins.values():
            plugin.setup(self.__root_parser)

    def __parse_arguments(self, arguments=sys.argv[1:]):
        self.__namespace = self.__root_parser.parse_args(arguments)

    @property
    def namespace(self):
        return self.__namespace


class _Setup(object):

    def __init__(self):
        self.__plugins = None  # type: _PluginStorage
        self.__arguments = None  # type: _ArgPrimer
        self.__child_interfaces = {}  # type: Dict[str, plugins.BasePlugin]
        self.__main_interface = None  # type: plugins.Main

    def create_main_program(self, plugins, arguments):
        # type: (_PluginStorage, _ArgPrimer) -> None
        self.__plugins = plugins
        self.__arguments = arguments
        self.__setup_children_plugins()
        self.__setup_main_plugin()

    def __setup_children_plugins(self):
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
        return self.__main_interface

class StartArguments(object):

    def __init__(self):
        self.__plugins = _PluginStorage()
        self.__arguments = _ArgPrimer()
        self.__setup = _Setup()

    def start(self, config):
        self.__plugins.load(config['name'])
        self.__arguments.prime_plugins(self.__plugins, config['description'])
        self.__setup.create_main_program(self.__plugins, self.__arguments)
        self.__setup.main.start()
