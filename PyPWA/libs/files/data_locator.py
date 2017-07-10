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
Here we use appdirs to determine the location of where data should be saved 
on the system for cache, data, and logs.
"""

import os

import appdirs

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _CheckLocationIsUsable(object):

    def find_usable_uri(self, potential_uri):
        # type: (str) -> str
        self.__recursively_make_uri_directories(potential_uri)
        return self.__determine_potential_or_cwd(potential_uri)

    @staticmethod
    def __recursively_make_uri_directories(potential_uri):
        # type: (str) -> None
        try:
            os.makedirs(potential_uri)
        except OSError:
            pass

    def __determine_potential_or_cwd(self, potential_uri):
        # type: (str) -> str
        try:
            self.__check_writable(potential_uri)
            return potential_uri
        except OSError:
            self.__check_writable(os.getcwd())
            return os.getcwd()

    @staticmethod
    def __check_writable(potential_uri):
        # type: (str) -> None
        test_file = potential_uri + "/test"
        with open(test_file, "w") as stream:
            stream.write("test")
        os.remove(test_file)


def get_cache_uri():
    # type: () -> str
    possible_uri = appdirs.user_cache_dir("PyPWA", "JLab", __version__)
    usable_location = _CheckLocationIsUsable()
    return usable_location.find_usable_uri(possible_uri)
