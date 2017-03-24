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

import pytest

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA import builtin_plugins
from PyPWA.core.configurator import options
from PyPWA.core.configurator.storage import core_storage
from PyPWA.core.shared import plugin_loader
from PyPWA.shell import fitting

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


@pytest.fixture()
def module_storage():
    return core_storage.ModuleStorage(None)


@pytest.fixture()
def metadata_storage():
    loader = plugin_loader.PluginStorage()
    loader.add_plugin_location(builtin_plugins)
    plugins = loader.get_by_class(options.Plugin)

    storage = core_storage.MetadataStorage()
    storage.add_plugins(plugins)
    return storage


def test_module_finds_shells(module_storage):
    assert len(module_storage.shell_modules) != 0


def test_module_finds_fitter(module_storage):
    assert fitting.ShellFitting in module_storage.shell_modules


def test_module_finds_options(module_storage):
    assert len(module_storage.option_modules) != 0


def test_metadata_storage_finds_builtin_parser(metadata_storage):
    object = metadata_storage.search_plugin(
        "Builtin Parser", options.Types.DATA_PARSER
    )
    assert issubclass(object, options.Plugin)


def test_metadata_storage_finds_optimizers(metadata_storage):
    object = metadata_storage.request_plugin_by_type(
        options.Types.OPTIMIZER
    )
    assert len(object) == 2