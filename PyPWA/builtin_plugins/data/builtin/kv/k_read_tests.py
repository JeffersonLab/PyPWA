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
Handles EVIL to / from memory.

The objects in this file are dedicated to reading the EVIL files from disk
and into memory. This file type is being depreciated for many reasons, and
will live here until it shrivels away, is completely forgotten, and dies.

EVIL, Expanded Variable Identification Lists, earned their name from their
inefficient nature when it comes to reading in, writing out, or simply
existing, its a name given to these EVIL formats out of a mixture of spite
and love by current and former developers alike.

This format exists currently only as backwards compatibility, and may not
be bug free or entirely optimized, and may never be. If you are a user
trying to figure out what you should export your data to, or a developer
trying to learn the nature of data within PyPWA, you should move your
attention to CSV/TSV in the SV object and forget that this ever existed.
"""

import io

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import data_templates
from PyPWA.builtin_plugins.data import exceptions

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class EVILDataTest(data_templates.ReadTest):
    _evil_type = str

    def _check_data_type(self, file_location):
        """
        Performs a really simple test to see if its a support format.

        Raises:
            PyPWA.libs.data.exceptions.IncompatibleData:
                Raised when the test fails to find a supported format.
        """
        the_file = io.open(file_location)
        test_data = the_file.readline().strip("\n")
        if "=" in test_data:
            self._evil_type = "DictOfArrays"
        elif "." in test_data and len(test_data) > 1:
            self._evil_type = "ListOfFloats"
        elif len(test_data) == 1:
            self._evil_type = "ListOfBools"
        else:
            raise exceptions.IncompatibleData("Failed to find a data")

    def quick_test(self, file_location):
        """
        Runs the various tests included tests.
        """
        self._check_data_type(file_location)

    def full_test(self, file_location):
        self.quick_test(file_location)

    @property
    def evil_type(self):
        """
        Property that returns the data type that was detected.

        Returns:
            str: The type of data the validator detected during its tests.
        """
        try:
            return self._evil_type
        except AttributeError:
            return False
