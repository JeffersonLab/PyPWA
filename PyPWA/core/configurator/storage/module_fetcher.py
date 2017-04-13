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
Allows the program to fetch plugins and mains by their name so that the 
names inside the configuration file can match up to their respected plugin.
"""

import logging

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator.storage import core_storage

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ModulePicking(core_storage.Storage):

    def __init__(self):
        super(ModulePicking, self).__init__()

    def request_main_by_id(self, the_id):
        for main in self._get_shells():
            if main.plugin_name == the_id:
                return main

    def request_plugin_by_name(self, name):
        for plugin in self._get_plugins():
            if plugin.plugin_name == name:
                return plugin
