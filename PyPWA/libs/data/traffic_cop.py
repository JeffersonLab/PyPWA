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

"""The utility objects for the Data Plugin

This holds all the main objects for the data plugin. This has search functions
but these objects should never know anything about the data plugin they are
trying to load, all it should ever care about is that there is metadata that
contains enough information about the plugin for this to get started passing
data to it.
"""

import logging

import ruamel.yaml
import ruamel.yaml.comments

from PyPWA.configuratr import tools
from PyPWA.libs.data import definitions
from PyPWA.libs.data import _utilites
from PyPWA.libs.data import builtin
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION

BUILTIN_PACKAGE_LOCATION = builtin

class Options(object):
    cache = True
    file_location = str
    fail = False

    def test_method(self):
        data_settings = ruamel.yaml.comments.CommentedMap()


class TrafficCop(object):

    def __init__(self, external_packages=False, global_settings=False):
        if isinstance(external_packages, str):
            packages = [external_packages, BUILTIN_PACKAGE_LOCATION]
        elif isinstance(external_packages, list):
            packages = external_packages + [BUILTIN_PACKAGE_LOCATION]
        else:
            packages = [BUILTIN_PACKAGE_LOCATION]

        if isinstance(global_settings, dict):
            global_settings = tools.lowercase_dict(global_settings)
            try:
                global_settings["cache"]


        plugins = self._index_packages(packages)
        self._search = _utilites.DataSearch(plugins)

        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())



    @staticmethod
    def _index_packages(packages):
        plugins = []
        loader = _utilites.FindPlugins()
        for package in packages:
            plugins.append(loader.find_plugin(package))

        return plugins

    def reader(self, file_location, event_iterator=False):
        the_plugin = self._search.search(file_location)
