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

import typing
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class PluginTypes(object):
    _NAMES = [
        # Internal name, External Name
        ["data parser", "Data Parsing"],
        ["data reader", "Data Iterator"],
        ["kernel processing", "Kernel Processor"],
        ["minimization", "Minimizer"]
    ]

    def internal_to_external(self, plugin_type: str) -> typing.List[str]: ...

    def external_to_internal(self, plugin_type: str) -> typing.List[str]: ...

    def internal_types(self) -> typing.List[str]: ...

    def external_types(self) -> typing.List[str]: ...
