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

import logging
import typing

import numpy
from PyPWA.builtin_plugins.data import data_templates


class PluginSearch(object):

    _logger = logging.getLogger(__name__)
    _found_plugins = typing.List[data_templates.TemplateDataPlugin]

    def __init__(self, user_plugin_dir: str): ...

    def _setup_plugin_storage(self, user_plugin_dir: str): ...

    def get_read_plugin(self, file_location: str) -> data_templates.TemplateDataPlugin: ...

    def get_write_plugin(self, file_location: str, data: numpy.ndarray) -> data_templates.TemplateDataPlugin: ...


class _FindReadPlugins(object):

    _logger = logging.getLogger(__name__)
    _potential_plugins = typing.List[data_templates.TemplateDataPlugin]

    def __init__(self, potential_plugins: typing.List[data_templates.TemplateDataPlugin]): ...

    def get_plugin(self, file_location: str) -> data_templates.TemplateDataPlugin: ...

    def _search_plugin_list(self, file_location: str) -> data_templates.TemplateDataPlugin: ...

    def _plugin_can_read(self, plugin: data_templates.TemplateDataPlugin, file_location: str) -> bool: ...

    def _run_read_test(self, plugin: data_templates.TemplateDataPlugin, file_location: str): ...


class _FindWritePlugins(object):

    _data_is_gamp = False
    _data_is_flat = False
    _file_extension = ""
    _logger = logging.getLogger(__name__)
    _potential_plugins = typing.List[data_templates.TemplateDataPlugin]

    def __init__(self, potential_plugins: typing.List[data_templates.TemplateDataPlugin]): ...

    def get_plugin(self, file_location: str, data: numpy.ndarray) -> data_templates.TemplateDataPlugin: ...

    def _set_data_type(self, data: numpy.ndarray): ...

    def _set_data_extension(self, file_location: str): ...

    def _search_for_plugins(self) -> data_templates.TemplateDataPlugin: ...

    def _check_plugin(self, the_plugin: data_templates.TemplateDataPlugin) -> bool: ...

    def _supports_data_type(self, plugin: data_templates.TemplateDataPlugin) -> bool: ...

    def _supports_file_extension(self, extensions: typing.List[str]) -> bool: ...
