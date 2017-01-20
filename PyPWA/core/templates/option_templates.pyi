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

import ruamel.yaml.comments

import typing
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
    __processed_options = ... # type: tools.ProcessOptions

    def __init__(self, processed_options):
        self.__processed_options = processed_options

    def _default_options(self)-> typing.Dict: ...

    def _option_levels(self) -> typing.Dict: ...

    def _option_types(self) -> typing.Dict: ...

    def _module_comment(self) -> typing.Dict: ...

    def _option_comments(self) -> typing.Dict: ...

    @staticmethod
    def _build_function(imports, function) -> typing.Dict: ...

    def request_options(self, level: str) -> \
            ruamel.yaml.comments.CommentedMap: ...

    def request_metadata(self, data: str) -> object: ...


class PluginsOptionsTemplate(_CoreOptionsParsing):

    def __init__(self): ...

    def _plugin_name(self) -> str: ...

    def _default_options(self) -> typing.Dict: ...

    def _option_levels(self) -> typing.Dict: ...

    def _option_types(self) -> typing.Dict: ...

    def _module_comment(self) -> str: ...

    def _option_comments(self) -> typing.Dict: ...

    def _plugin_interface(self) -> object: ...

    def _plugin_type(self) -> str: ...

    def _user_defined_function(self) -> typing.Dict: ...

    def request_metadata(self, data) -> object: ...


class MainOptionsTemplate(_CoreOptionsParsing):

    _shell_main = "main shell"
    _gui_main = "main gui"

    def __init__(self): ...

    def _shell_id(self) -> str: ...

    def _default_options(self) -> typing.Dict: ...

    def _option_levels(self) -> typing.Dict: ...

    def _option_types(self) -> typing.Dict: ...

    def _module_comment(self) -> str: ...

    def _option_comments(self) -> typing.Dict: ...

    def _main_type(self) -> str: ...

    def _user_defined_function(self) -> typing.Dict: ...

    def _interface_object(self) -> object: ...

    def _requires_data_parser(self) -> bool: ...

    def _requires_kernel_processing(self) -> bool: ...

    def _requires_minimization(self) -> bool: ...

    def _requires_data_reader(self) -> bool: ...

    def request_metadata(self, data: str) -> object: ...

    def requires(self, the_type: str) -> bool: ...
