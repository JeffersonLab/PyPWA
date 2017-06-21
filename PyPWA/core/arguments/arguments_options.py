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
Provides a simple interface for Main Objects in the ArgumentParser
"""

import argparse
from typing import List
from typing import Optional as Opt

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Base(object):

    def get_name(self):
        raise NotImplementedError


class Plugin(Base):

    def __init__(self):
        self._parser = None   # type: argparse.ArgumentParser
        self.__name = None  # type: str

    def setup(self, parser, name):
        # type: (argparse.ArgumentParser, str) -> None
        self._parser = parser.add_argument_group(name)
        self.__name = name
        self._add_arguments()

    def _add_arguments(self):
        raise NotImplementedError

    def get_plugin(self, parsed_values):
        # type: (dict) -> object
        raise NotImplementedError

    def get_name(self):
        # type: () -> str
        return self.__name


class Main(Base):

    def __init__(self):
        self._parser = None  # type: argparse.ArgumentParser
        self.__name = None  # type: str
        self.__required = None  # type: Opt[List[str]]

    def setup(self, parser, name, required=None):
        # type: (argparse.ArgumentParser, str, Opt[List[str]]) -> None
        self._parser = parser
        self.__name = name
        self.__required = required
        self._add_arguments()

    def _add_arguments(self):
        raise NotImplementedError

    def get_name(self):
        # type: () -> str
        return self.__name

    def get_required(self):
        # type: () -> Opt[List[str]]
        return self.__required
