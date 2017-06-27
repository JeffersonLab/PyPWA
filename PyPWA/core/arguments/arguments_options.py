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
Interfaces for Argument Parser
------------------------------
Contains all the necessary interfaces to implement a plugin that can be
used inside the argument parser.

- Base - This is the root plugin interface for all arg parse plugins. You
  really shouldn't implement this unless you know what you are doing. It's
  setup for code shared between the two main plugin types, Main and Plugin.
- Plugin - An interface that depends on Argument Groups.
- Main - An interface for main plugins, this arguments are added straight to
  the root of the plugin, and will appear as essential arguments.
"""

from argparse import ArgumentParser, Namespace
from typing import Dict, List
from typing import Optional as Opt

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Base(object):

    _NAME = NotImplemented  # type: str

    def __init__(self):
        self._parser = None  # type: ArgumentParser

    def setup(self, parser):
        raise NotImplementedError

    def _add_arguments(self):
        raise NotImplementedError

    def get_name(self):
        # type: () -> str
        return self._NAME


class Plugin(Base):

    def setup(self, parser):
        # type: (ArgumentParser) -> None
        self._parser = parser.add_argument_group(self.get_name())
        self._add_arguments()

    def get_interface(self, namespace):
        # type: (Namespace) -> plugins.BasePlugin
        raise NotImplementedError


class Main(Base):

    _REQUIRED = None  # type: List[Opt[str]]

    def setup(self, parser):
        # type: (ArgumentParser) -> None
        self._parser = parser
        self._add_arguments()

    def get_required(self):
        # type: () -> List[Opt[str]]
        return self._REQUIRED

    def get_interface(self, namespace, plugins):
        # type: (Namespace, Dict[str, plugins.BasePlugin]) -> plugins.Main
        raise NotImplementedError
