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

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.builtin_plugins.data import _plugin_finder
from PyPWA.builtin_plugins.data import exceptions
from PyPWA.core.templates import plugin_templates
from PyPWA.builtin_plugins.data.cache import _builder

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Memory(plugin_templates.DataParserTemplate):

    _enable_cache = True
    _clear_cache = False
    _user_plugin_dir = ""
    _logger = logging.getLogger(__name__)
    _plugin_search = _plugin_finder.PluginSearch
    _cache_builder = _builder.CacheBuilder
    _cache_interface = _builder._CacheInterface

    def __init__(
            self, enable_cache=True, clear_cache=False,
            user_plugin_dir="", **options
    ):
        self._logger.addHandler(logging.NullHandler())

        self._enable_cache = enable_cache
        self._clear_cache = clear_cache
        self._user_plugin_dir = user_plugin_dir

        if options:
            super(Memory, self).__init__(options=options)

        self._set_plugin_search()
        self._set_cache_plugin()

    def _set_plugin_search(self):
        self._plugin_search = _plugin_finder.PluginSearch(
            self._user_plugin_dir
        )

    def _set_cache_plugin(self):
        self._cache_builder = _builder.CacheBuilder(
            self._enable_cache, self._clear_cache
        )

    def parse(self, file_location):
        self._set_cache_interface(file_location)
        if self._cache_interface.is_valid:
            self._logger.info("Found Cache, loading!")
            return self._cache_interface.read_cache()
        else:
            self._logger.info("No cache found, loading file directly.")
            return self._parse_with_cache(file_location)

    def _set_cache_interface(self, file_location):
        self._cache_interface = self._cache_builder.get_cache_interface(
            file_location
        )

    def _parse_with_cache(self, file_location):
        data = self._read_data(file_location)
        self._cache_interface.write_cache(data)
        return data

    def _read_data(self, file_location):
        plugin = self._load_read_plugin(file_location)
        returned_parser = plugin.get_plugin_memory_parser()
        return returned_parser.parse(file_location)

    def _load_read_plugin(self, file_location):
        try:
            return self._plugin_search.get_read_plugin(file_location)
        except exceptions.UnknownData:
            raise OSError

    def write(self, file_location, data):
        self._set_cache_interface(file_location)
        self._write_data(file_location, data)
        self._cache_interface.write_cache(data)

    def _write_data(self, file_location, data):
        plugin = self._load_write_plugin(file_location, data)
        found_parser = plugin.get_plugin_memory_parser()
        found_parser.write(file_location, data)

    def _load_write_plugin(self, file_location, data):
        try:
            return self._plugin_search.get_write_plugin(file_location, data)
        except exceptions.UnknownData:
            raise RuntimeError
