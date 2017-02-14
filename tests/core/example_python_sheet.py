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

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core.templates import option_templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


def the_meaning_of_life():
    return 42


def what_is_the_internet_ran_by():
    return "cats"


def the_best_gaming_console(vendor=False):
    if vendor == "microsoft":
        return "linux"
    else:
        return "sony"


class OptionsTest(option_templates.PluginsOptionsTemplate):

    def _plugin_name(self):
        return "Does not exist"

    def _default_options(self):
        return {}

    def _option_levels(self):
        return {}

    def _module_comment(self):
        return "I think, therefore I am."

    def _option_comments(self):
        return {}

    def _plugin_interface(self):
        return the_best_gaming_console

    def _plugin_type(self):
        return self._kernel_processing

    def _user_defined_function(self):
        return False
