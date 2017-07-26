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
Simple writers to export configurations.
----------------------------------------

- _YmlWriter - Exports configurations using ruamel.yaml, this is default, and
  is the only way to get comments.
  
- _JsonWriter - Exports configurations using json for masochists who prefer 
  it, does not support comments.
  
- Write - Simple wrapping main object around the two defined writers.
"""

import json
import os
from typing import Any, Dict

import ruamel.yaml

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _YmlWriter(object):

    @staticmethod
    def write(settings, location):
        # type: (Dict[str, Any], str) -> None
        with open(location, "w") as stream:
            stream.write(
                ruamel.yaml.dump(
                    settings,
                    Dumper=ruamel.yaml.RoundTripDumper
                )
            )


class _JsonWriter(object):

    @staticmethod
    def write(settings, location):
        # type: (Dict[str, Any], str) -> None
        with open(location, "w") as stream:
            stream.write(json.dumps(settings, indent=4))


class Write(object):

    def __init__(self):
        self.__json = _JsonWriter()
        self.__yml = _YmlWriter()

    def write(self, settings, location):
        # type: (Dict[str, Any], str) -> None
        if self.__is_json(location):
            self.__json.write(settings, location)
        else:
            self.__yml.write(settings, location)

    @staticmethod
    def __is_json(location):
        # type: (str) -> bool
        if os.path.splitext(location)[1] == ".json":
            return True
        else:
            return False
