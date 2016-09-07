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
Simple Tests for Configurator

See Also:
    PyPWA.configurator.configurator
"""
import PyPWA.libs

from PyPWA.configurator import configurator, plugin_loader, templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"


def test_MetadataStorage_LoadPluginsRandomPlugins_PluginsSorted():
    loader = plugin_loader.PluginLoading(templates.OptionsTemplate)
    plugin_list = loader.fetch_plugin([PyPWA.libs])

    metadata_storage = configurator.MetadataStorage()
    metadata_storage.add_plugins(plugin_list)

    assert len(metadata_storage.data_parser) == 1
    assert len(metadata_storage.data_reader) == 1
    assert len(metadata_storage.minimization) == 2
    assert len(metadata_storage.kernel_processing) == 1
