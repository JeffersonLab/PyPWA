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
Holds the different implementation interfaces that are needed to interface
data module.
"""

from typing import List

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import internals

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class TemplateDataPlugin(object):

    @property
    def plugin_name(self):
        # type: () -> str
        raise NotImplementedError()

    def get_plugin_memory_parser(self):
        # type: () -> TemplateMemory
        raise NotImplementedError()

    def get_plugin_reader(self, file_location):
        # type: (str) -> internals.Reader
        raise NotImplementedError()

    def get_plugin_writer(self, file_location):
        # type: (str) -> internals.Writer
        raise NotImplementedError()

    def get_plugin_read_test(self):
        # type: () -> ReadTest
        raise NotImplementedError()

    @property
    def plugin_supported_extensions(self):
        # type: () -> List[str]
        raise NotImplementedError()

    @property
    def plugin_supports_flat_data(self):
        # type: () -> bool
        raise NotImplementedError()

    @property
    def plugin_supports_gamp_data(self):
        # type: () -> bool
        raise NotImplementedError()


class TemplateMemory(object):

    def parse(self, file_location):
        # type: (str) -> numpy.ndarray
        raise NotImplementedError()

    def write(self, file_location, data):
        # type: (str, numpy.ndarray) -> None
        raise NotImplementedError()


class ReadTest(object):

    def quick_test(self, file_location):
        # type: (str) -> None
        """
        Raises:
            PyPWA.builtin_plugins.data.exceptions.IncompatibleData: Raised
                when data  failed to test properly for the file.
        """
        raise NotImplementedError()

    def full_test(self, file_location):
        # type: (str) -> None
        """
        Raises:
            PyPWA.builtin_plugins.data.exceptions.IncompatibleData: Raised
                when data  failed to test properly for the file.
        """
        raise NotImplementedError()
