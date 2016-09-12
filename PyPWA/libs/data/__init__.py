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
This module loads data from various data types to be used
inside the program as they would like. Data types supported
are the classic Kinematic Variable files defined by Josh
Pond, the QFactors List, the Weight list, the Condensed
single line Weight, and the Tab or Comma separated
kinematic variables.

Examples:
    To load data from file:
        file = PyPWA.data.file_manager.MemoryInterface()
        file.parse(path_to_file)
    To write data to file:
        file = PyPWA.data.file_manager.MemoryInterface()
        file.write(path_to_file, the_data)
"""
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core_libs.templates import option_templates
from PyPWA.libs.data import traffic_cop

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class DataParser(option_templates.PluginsOptionsTemplate):

    def _plugin_name(self):
        return traffic_cop.MODULE_NAME

    def _plugin_interface(self):
        return traffic_cop.Memory

    def _plugin_type(self):
        return self._data_parser

    def _default_options(self):
        return {
            "cache": True,
            "clear cache": False,
            "fail": False,
            "user plugin": "cwd=/path/to/file;"
        }

    def _option_levels(self):
        return {
            "cache": self._optional,
            "clear cache": self._advanced,
            "fail": self._advanced,
            "user plugin": self._advanced
        }

    def _option_types(self):
        return {
            "cache": bool,
            "clear cache": bool,
            "fail": bool,
            "user plugin": str
        }

    def _main_comment(self):
        return "This is the builtin data parser, you can replace " \
               "this with your own data parser if you wish."

    def _option_comments(self):
        return {
            "cache":
                "Should Cache be enabled? The cache will automatically "
                "clear if it detects a change in any of your data and "
                "should be safe to leave enabled.",
            "clear cache":
                "Should we force the cache to clear? This will destroy "
                "all of your caches, this means loading your data will "
                "take much longer, its recommended to leave this off "
                "unless you are certain its a cache issue.",
            "fail":
                "Should the program stop if it fails to load the file? "
                "The program will already fail if the data is needed for "
                "parsing to happen, if this is set to true even files "
                "that are optional will cause the program to stop.",
            "user plugin":
                "A plugin that can be loaded into the the " +
                traffic_cop.MODULE_NAME + " for parsing, see the "
                "documentation on the " + traffic_cop.MODULE_NAME +
                " plugin for more information."
        }


class DataIterator(option_templates.PluginsOptionsTemplate):

    def _plugin_name(self):
        return traffic_cop.MODULE_NAME

    def _plugin_interface(self):
        return traffic_cop.Iterator

    def _plugin_type(self):
        return self._data_reader

    def _user_defined_function(self):
        return None

    def _default_options(self):
        return {
            "fail": False,
            "user plugin": "cwd=/path/to/file;"
        }

    def _option_levels(self):
        return {
            "fail": self._advanced,
            "user plugin": self._advanced
        }

    def _option_types(self):
        return {
            "fail": bool,
            "user plugin": str
        }

    def _main_comment(self):
        return "This is the builtin data parser, you can replace " \
               "this with your own data parser if you wish."

    def _option_comments(self):
        return {
            "fail":
                "Should the program stop if it fails to load the file? "
                "The program will already fail if the data is needed for "
                "parsing to happen, if this is set to true even files "
                "that are optional will cause the program to stop.",
            "user plugin":
                "A plugin that can be loaded into the the " +
                traffic_cop.MODULE_NAME + " for parsing, see the "
                "documentation on the " + traffic_cop.MODULE_NAME +
                " plugin for more information."
        }