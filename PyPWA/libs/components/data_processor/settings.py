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
Main object for Parsing Data
"""

from typing import Dict

from PyPWA import AUTHOR, VERSION
from PyPWA.libs import configuration_db

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class DataSettings(object):

    def __init__(self):
        self.__db = configuration_db.Connector()
        self.__initialize_defaults()

    def __initialize_defaults(self):
        self.__db.initialize_component(
            "Data Processor",
            {
                "use cache": True,
                "clear cache": False
            }
        )

    def merge_settings(self, settings):
        # type: (Dict[str, bool]) -> None
        self.__db.merge_component("Data Processor", settings)

    def use_cache(self, enable=True):
        self.__db.modify_setting("Data Processor", "use cache", enable)

    def clear_cache(self, enable=False):
        self.__db.modify_setting("Data Processor", "clear cache", enable)
