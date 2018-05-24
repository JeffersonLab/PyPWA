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

from typing import Union

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.initializers.arguments import arguments_options
from PyPWA.initializers.configurator import options
from PyPWA.libs.components.data_processor import settings
from PyPWA.libs.math import particle

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION

SUPPORTED_DATA_TYPE = Union[numpy.ndarray, particle.ParticlePool]


class DataConf(options.Component):

    def __init__(self):
        super(DataConf, self).__init__()
        self.name = "Data Processor"
        self.module_comment = "Parses raw text and numpy data."

    def get_default_options(self):
        return  {
            "use cache": True,
            "clear cache": False,
            "user plugin": None
        }

    def get_option_difficulties(self):
        return {
            "use cache": options.Levels.OPTIONAL,
            "clear cache": options.Levels.ADVANCED,
            "user plugin": options.Levels.ADVANCED
        }

    def get_option_types(self):
        return {
            "use cache": bool,
            "clear cache": bool,
            "user plugin": str
        }

    def get_option_comments(self):
        return {
            "use cache": "Enable caching of all read data.",
            "clear cache":
                "Force cache to be cleared even if the data file hasn't "
                "changed.",
            "user plugin":
                "Directory that has potential plugins for the data parser in "
                "it. Read the docs for more information."
        }


class DataArg(arguments_options.Component):

    _NAME = "Data Processor"

    def __init__(self):
        self.__settings =settings.DataSettings()
        super(DataArg, self).__init__()

    def _add_arguments(self):
        self.__add_enable_cache()
        self.__add_clear_cache()

    def __add_enable_cache(self):
        self._parser.add_argument(
            "--use-cache", action='store_true', default=False,
            help="Enable caching of interacted data. This will speed up "
                 "future interaction with the same data."
        )

    def __add_clear_cache(self):
        self._parser.add_argument(
            "--clear-cache", action="store_true", default=False,
            help="Force cache for interacted files to be cleared."
        )

    def setup_db(self, namespace):
        self.__settings.merge_settings(
            {
                "use cache": namespace.use_cache,
                "clear cache": namespace.clear_cache
            }
        )
