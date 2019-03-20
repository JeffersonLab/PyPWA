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
Contains PluginSearch and helper private classes. This file is used to load
the data plugins and user plugins then return one of them that can read/write
whatever data needs to be read/written.

- PluginSearch - Searches for data plugins that can read or write the provided
  data.

- _FindReadPlugins - searches for a plugin that can read the provided data.

- _FindWritePlugins - Searches for a plugin that can write the given data
  to the given file extension.
"""

import logging

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs import plugin_loader
from PyPWA.plugins import data
from . import data_templates

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class PluginSearch(object):

    __LOGGER = logging.getLogger(__name__ + ".PluginSearch")

    def __init__(self):
        self.__found_plugins = plugin_loader.fetch_plugins(data, "Data")

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

    def get_read_plugin(self, filename):
        # type: (Path) -> data_templates.DataPlugin
        for plugin in self.__found_plugins:
            if plugin.get_read_test().can_read(filename):
                self.__LOGGER.debug(
                    "Using {0} to load {1}".format(
                        plugin.plugin_name, filename
                    )
                )
                return plugin
        raise RuntimeError("Couldn't find plugin for {0}".format(filename))

    def get_write_plugin(self, filename, data_type):
        # type: (Path, data_templates.DataType) -> data_templates.DataPlugin
        for plugin in self.__found_plugins:
            if data_type in plugin.supported_data_types:
                extension = filename.suffix
                if not extension or extension in plugin.supported_extensions:
                    return plugin
        raise RuntimeError("Couldn't find plugin for {0}".format(filename))
