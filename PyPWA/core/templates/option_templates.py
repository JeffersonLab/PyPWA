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

"""

from PyPWA.core import tools
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _CoreOptionsParsing(object):

    _required = "required"
    _optional = "optional"
    _advanced = "advanced"
    _kernel_processing = "kernel processing"
    _minimization = "minimization"
    _data_reader = "data reader"
    _data_parser = "data parser"
    __processed_options = tools.ProcessOptions

    def __init__(self, processed_options):
        self.__processed_options = processed_options

    def _default_options(self):
        raise NotImplementedError

    def _option_levels(self):
        raise NotImplementedError

    def _option_types(self):
        raise NotImplementedError

    def _module_comment(self):
        raise NotImplementedError

    def _option_comments(self):
        raise NotImplementedError

    @staticmethod
    def _build_function(imports, function):
        return {"function": function, "imports": set(imports)}

    def request_options(self, level):
        return {
            "required": self.__processed_options.required,
            "optional": self.__processed_options.optional,
            "advanced": self.__processed_options.advanced,
            "template": self._option_types()
        }[level]

    def request_metadata(self, data):
        raise NotImplementedError


class PluginsOptionsTemplate(_CoreOptionsParsing):

    def __init__(self):
        processed_options = tools.ProcessOptions(
            self._plugin_name(), self._module_comment(),
            self._option_comments(), self._option_types(),
            self._default_options(), self._option_levels()
        )

        super(PluginsOptionsTemplate, self).__init__(processed_options)

    def _plugin_name(self):
        raise NotImplementedError

    def _default_options(self):
        raise NotImplementedError

    def _option_levels(self):
        raise NotImplementedError

    def _option_types(self):
        raise NotImplementedError

    def _module_comment(self):
        raise NotImplementedError

    def _option_comments(self):
        raise NotImplementedError

    def _plugin_interface(self):
        raise NotImplementedError

    def _plugin_type(self):
        raise NotImplementedError

    def _user_defined_function(self):
        raise NotImplementedError

    def request_metadata(self, data):
        return {
            "name": self._plugin_name(),
            "interface": self._plugin_interface(),
            "provides": self._plugin_type(),
            "user functions": self._user_defined_function()
        }[data]


class MainOptionsTemplate(_CoreOptionsParsing):

    _shell_main = "main shell"
    _gui_main = "main gui"

    def __init__(self):
        processed_options = tools.ProcessOptions(
            self._shell_id(), self._module_comment(),
            self._option_comments(), self._option_types(),
            self._default_options(), self._option_levels()
        )

        super(MainOptionsTemplate, self).__init__(processed_options)

    def _shell_id(self):
        raise NotImplementedError

    def _default_options(self):
        raise NotImplementedError

    def _option_levels(self):
        raise NotImplementedError

    def _option_types(self):
        raise NotImplementedError

    def _module_comment(self):
        raise NotImplementedError

    def _option_comments(self):
        raise NotImplementedError

    def _main_type(self):
        raise NotImplementedError

    def _user_defined_function(self):
        raise NotImplementedError

    def _interface_object(self):
        raise NotImplementedError

    def _requires_data_parser(self):
        raise NotImplementedError

    def _requires_kernel_processing(self):
        raise NotImplementedError

    def _requires_minimization(self):
        raise NotImplementedError

    def _requires_data_reader(self):
        raise NotImplementedError

    def request_metadata(self, data):
        return {
            "id": self._shell_id(),
            "ui": self._main_type(),
            "object": self._interface_object(),
            "user functions": self._user_defined_function()
        }[data]

    def requires(self, the_type):
        return {
            self._data_parser: self._requires_data_parser(),
            self._data_reader: self._requires_data_reader(),
            self._kernel_processing: self._requires_kernel_processing(),
            self._minimization: self._requires_minimization()
        }[the_type]
