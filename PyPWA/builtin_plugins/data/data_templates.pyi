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

import numpy
import typing
from PyPWA.core.templates import interface_templates


class TemplateDataPlugin(object):

    @property
    def plugin_name(self) -> str: ...

    def get_plugin_memory_parser(self) -> TemplateMemory(): ...

    def get_plugin_reader(self, file_location: str) -> interface_templates.ReaderInterfaceTemplate(): ...

    def get_plugin_writer(self, file_location: str) -> interface_templates.WriterInterfaceTemplate(): ...

    def get_plugin_read_test(self) -> ReadTest(): ...

    @property
    def plugin_supported_extensions(self) -> typing.List[str]: ...

    @property
    def plugin_supports_flat_data(self) -> bool: ...

    @property
    def plugin_supports_gamp_data(self) -> bool: ...


class TemplateMemory(object):
    def parse(self, file_location: str) -> numpy.ndarray: ...

    def write(self, file_location: str, data: numpy.ndarray): ...


class ReadTest(object):

    def quick_test(self, file_location: str): ...

    def full_test(self, file_location: str): ...
