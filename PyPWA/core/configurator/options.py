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

import enum

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Types(enum.Enum):
    KERNEL_PROCESSING = 1
    OPTIMIZER = 2
    DATA_READER = 3
    DATA_PARSER = 4
    SKIP = 5


class Levels(enum.Enum):
    REQUIRED = 1
    OPTIONAL = 2
    ADVANCED = 3


class Setup(object):

    def return_interface(self):
        raise NotImplementedError


class Base(object):
    plugin_name = "BASE"
    default_options = {}
    option_difficulties = {}
    option_types = {}
    module_comment = "BASE"
    option_comments = {}
    defined_function = None


class Plugin(Base):
    setup = Setup  # type: Setup
    provides = Types.SKIP  # type: Types


class Main(Base):
    setup = None  # type: Setup
    required_plugins = []  # type: [Types]
