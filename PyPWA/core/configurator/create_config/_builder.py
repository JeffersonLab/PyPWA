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

.. todo::
   Refactor this entire file.

- ConfigurationBuilder - Actually holds the questions being asked.

- _AskForSpecificPlugin - Handles selecting the plugin needed when there is 
  more than one plugin when it can.
  
- PluginList - Returns a list of all the plugins.
"""

import ruamel.yaml.comments

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator.create_config import _level_processing
from PyPWA.core.configurator.create_config import _override

__credits__ = ["Mark Jones", "Ryan Wright"]
__author__ = AUTHOR
__version__ = VERSION


class BuildConfig(object):

    __configuration = ruamel.yaml.comments.CommentedMap()
    __level_fetch = _level_processing.ProcessOptions()
    __overrider = _override.Override()

    __plugin_list = None
    __level = None

    def __init__(self, plugin_list, level):
        self.__plugin_list = plugin_list
        self.__level = level

    def build(self, overrides):
        self.__create_configuration()
        self.__overrider.execute(self.__configuration, overrides)

    def __create_configuration(self):
        self.__update_shell()
        self.__update_plugins()

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
        return self.__level_fetch.processed_options(
            plugin, self.__level.get_plugin_level()
        )

    @property
    def configuration(self):
        return self.__overrider.processed_configuration
