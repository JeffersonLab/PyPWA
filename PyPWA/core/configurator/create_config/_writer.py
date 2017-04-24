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

import os
import json
import ruamel.yaml

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _YmlWriter(object):

    @staticmethod
    def write(settings, location):
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
        with open(location, "w") as stream:
            stream.write(json.dumps(settings, indent=4))


class Write(object):
    __json = _JsonWriter()
    __yml = _YmlWriter()

    def write(self, settings, location):
        if self.__is_json(location):
            self.__json.write(settings, location)
        else:
            self.__yml.write(settings, location)

    @staticmethod
    def __is_json(location):
        if os.path.splitext(location)[1] == ".json":
            return True
        else:
            return False