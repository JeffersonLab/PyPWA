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

from PyPWA.builtin_plugins.data import memory
from PyPWA.builtin_plugins.data import iterator
from PyPWA.core.arguments import arguments_options
from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import _setups
from PyPWA.core.configurator import options

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class DataParser(options.Plugin):

    plugin_name = "Builtin Parser"
    setup = _setups.SetupParser
    provides = options.Types.DATA_PARSER
    defined_function = None
    module_comment = "Parses TSV, CSV, Kvs, and GAMP data."

    default_options = {
        "enable cache": True,
        "clear cache": False,
        "user plugin": None
    }

    option_difficulties = {
        "enable cache": options.Levels.OPTIONAL,
        "clear cache": options.Levels.ADVANCED,
        "user plugin": options.Levels.ADVANCED
    }

    option_types = {
        "enable cache": bool,
        "clear cache": bool,
        "user plugin": str
    }

    option_comments = {
        "enable cache": "Enable caching of all read data.",
        "clear cache":
            "Force cache to be cleared even if the data file hasn't changed.",
        "user plugin":
            "Directory that has potential plugins for the data parser in "
            "it. Read the docs for more information."
    }


class DataIterator(options.Plugin):

    plugin_name = "Builtin Iterator"
    setup = _setups.SetupIterator
    provides = options.Types.DATA_READER
    defined_function = None
    module_comment = "Iterates over TSV, CSV, Kvs, and GAMP data."

    default_options = {
        "fail": False,
        "user plugin": None
    }

    option_difficulties = {
        "fail": options.Levels.ADVANCED,
        "user plugin": options.Levels.ADVANCED
    }

    option_types = {
        "fail": bool,
        "user plugin": str
    }

    option_comments = {
        "fail":
            "Force Parser to crash when it fails to read a file even if "
            "a fallback exists.",
        "user plugin":
            "Directory that has potential plugins for the data parser in "
            "it. Read the docs for more information."
    }


class ArgDataParse(arguments_options.Plugin):

    _NAME = "Builtin Parser"

    def _add_arguments(self):
        self.__add_enable_cache()
        self.__add_clear_cache()

    def __add_enable_cache(self):
        self._parser.add_argument(
            "--cache", action='store_true', default=False,
            help="Enable caching of interacted data. This will speed up "
                 "future interaction with the same data."
        )

    def __add_clear_cache(self):
        self._parser.add_argument(
            "--clearcache", action="store_true", default=False,
            help="Force cache for interacted files to be cleared."
        )

    def get_interface(self, namespace):
        return memory.Memory(
            enable_cache=namespace.cache, clear_cache=namespace.clearcache
        )


class ArgDataIterate(arguments_options.Plugin):

    _NAME = "Builtin Iterator"

    def _add_arguments(self):
        pass

    def get_interface(self, namespace):
        return iterator.Iterator()
