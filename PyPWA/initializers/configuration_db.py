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

"""

import json
import copy
import warnings

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _Database(object):

    """
    This uses two dictionaries to handle *ALL* configuration for PyPWA.
    Everything that is and can ever be is here.

    This doesn't only store the options, but tracks there changes over the
    run of the program; This should allow us to debug issues when a failure
    occurs, or maybe in the future allow users to row back their changes to a
    previous configuration.

    Layout:
    __data = {
        "0": {
            "Component": {
                "Options": ...
            }
            "Another Component": {
                "Options": ...
            }
        }
        "1": {
            "Component": ...
        }
    }

    __index = 1

    """

    data = {0: dict()}
    index = 0


class Connector(object):

    __db = _Database()

    def purge(self):
        warnings.warn(
            "Purging the database could break the application!",
            RuntimeWarning
        )
        self.__db.index = 0
        self.__db.data.clear()
        self.__db.data[0] = dict()

    def initialize_component(self, component, configuration):
        self.__increment_reference()
        if component in self.__db.data[self.__db.index].keys():
            self.__override_component(component, configuration)
        else:
            self.__add_component(component, configuration)

    def __increment_reference(self):
        old_data = copy.deepcopy(self.__db.data[self.__db.index])
        self.__db.data[self.__db.index + 1] = old_data
        self.__db.index += 1

    def __override_component(self, component, configuration):
        if isinstance(self.__db.data[self.__db.index][component], dict):
            self.__db.data[self.__db.index][component].clear()
        self.__db.data[self.__db.index][component] = configuration

    def __add_component(self, component, configuration):
        self.__db.data[self.__db.index][component] = configuration

    def merge_component(self, component, configuration):
        self.__increment_reference()
        self.__db.data[self.__db.index][component].update(configuration)

    def modify_setting(self, component, setting, value):
        self.__increment_reference()
        self.__db.data[self.__db.index][component][setting] = value

    def read(self, component=None, setting=None):
        if component and setting:
            return self.__db.data[self.__db.index][component][setting]
        elif component:
            return self.__db.data[self.__db.index][component]
        else:
            return self.__db.data[self.__db.index]

    def crash_report(self):
        return json.dumps(self.__db.data.copy(), indent=2)
