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
Creates the configuration
-------------------------

- _GlobalOptions - Setups the global options if any are required.
- BuildConfig - The main object that builds the configuration.
"""

from typing import Any, Dict

import ruamel.yaml.comments

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import options
from PyPWA.core.configurator.create_config import _level_processing
from PyPWA.core.configurator.create_config import _metadata
from PyPWA.core.configurator.create_config import _override
from PyPWA.core.configurator.create_config import _questions

__credits__ = ["Mark Jones", "Ryan Wright"]
__author__ = AUTHOR
__version__ = VERSION


class _GlobalOptions(object):

    def __init__(self):
        self.__global_options = {"Global Options": {"plugin directory": ""}}

    def build_options(self, plugin_dir):
        # type: (_questions.GetPluginDirectory) -> None
        if plugin_dir.get_plugin_directory():
            self.__set_plugin_dir(plugin_dir)
        else:
            self.__global_options = None

    def __set_plugin_dir(self, plugin_dir):
        # type: (_questions.GetPluginDirectory) -> None
        self.__global_options["Global Options"]["plugin directory"] = \
            plugin_dir.get_plugin_directory()

    @property
    def global_options(self):
        # type: () -> Dict[str, Any]
        return self.__global_options


class BuildConfig(object):

    def __init__(
            self,
            plugin_dir,  # type: _questions.GetPluginDirectory
            plugin_list,   # type: _metadata.GetPluginList
            level  # type: options.Levels
    ):
        # type: (...) -> None
        self.__global = _GlobalOptions()
        self.__configuration = ruamel.yaml.comments.CommentedMap()
        self.__level_fetch = _level_processing.ProcessOptions()
        self.__overrider = _override.Override()
        self.__plugin_dir = plugin_dir
        self.__plugin_list = plugin_list
        self.__level = level

    def build(self, overrides):
        # type: (Dict[str, Any]) -> None
        self.__create_configuration()
        self.__overrider.execute(self.__configuration, overrides)

    def __create_configuration(self):
        self.__update_shell()
        self.__update_plugins()

    def __update_global_options(self):
        self.__global.build_options(self.__plugin_dir)
        if self.__global.global_options:
            self.__configuration.update(self.__global.global_options)

    def __update_shell(self):
        self.__configuration.update(
            self.__get_plugin_options(self.__plugin_list.shell)
        )

    def __update_plugins(self):
        for plugin in self.__plugin_list.plugins:
            self.__configuration.update(
                self.__get_plugin_options(plugin)
            )

    def __get_plugin_options(self, plugin):
        # type: (options.Base) -> Dict[str, Any]
        return self.__level_fetch.processed_options(
            plugin, self.__level.get_plugin_level()
        )

    @property
    def configuration(self):
        # type: () -> Dict[str, Any]
        return self.__overrider.processed_configuration
