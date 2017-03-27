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
Gamp data reading and writing.

This file holds the Gamp Reader and Gamp Writer. These simply load the
data into memory one event at a time and write to file one event at a
time. Only the previous loaded events are stored, anything later than that
will not be saved in memory by these object.
"""

import io

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import data_templates
from PyPWA.builtin_plugins.data import exceptions

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class GampDataTest(data_templates.ReadTest):

    def _check_events(self, file_location):
        """
        Checks the events to ensure that the number of particles match the
        number declared by the event.

        Raises:
            PyPWA.libs.data.exceptions.IncompatibleData:
                Raised when the tests fail for this object and the data.
        """
        the_file = io.open(file_location)
        count = 0
        while True:
            # Limit how much of the file is tested
            if count == 3:
                break
            number = the_file.readline().strip("\n").strip()

            # If the test has run at least once and has reached the end
            # then end the test
            if count and number == "":
                break

            # If we failed to find the particle count when it was
            # expected end the test with a fail.
            try:
                int(number)
            except ValueError as Error:
                raise exceptions.IncompatibleData(
                    "Expected particle count. Found " + repr(Error) +
                    str(count)
                )

            # If we failed to find all the particle data where it was
            # expected then end the test with a fail
            try:
                for index in range(int(number)):
                    data_length = len(the_file.readline().split(" "))
                    if data_length != 6:
                        raise ValueError(
                            "Particle doesn't have all the data "
                            "required by the gamp standard. Has " +
                            repr(data_length) + " at index " + repr(index)
                        )

            except Exception as Error:
                raise exceptions.IncompatibleData(
                    "Unexpected exception raised, caught " + repr(Error) +
                    " where it wasn't expected."
                )

            count += 1

    @staticmethod
    def _test_length(file_location):
        """
        Tests to make sure that the first number matches the number of
        events. I know that this can be made to be better, however it
        alludes me at this moment.

        Raises:
            PyPWA.libs.data.exceptions.IncompatibleData:
                Raised when the tests fail for this object and the data.
        """
        the_file = io.open(file_location)
        while True:
            number = the_file.readline().strip().strip("\n")
            try:
                if number == "":
                    break
                for index in range(int(number)):
                    the_file.readline()
            except Exception as Error:
                raise exceptions.IncompatibleData(
                    "Unexpected exception raised, caught " + str(Error) +
                    " where it wasn't expected."
                )

    def quick_test(self, text_file):
        self._test_length(text_file)
        self._check_events(text_file)

    def full_test(self, text_file):
        self.quick_test(text_file)
