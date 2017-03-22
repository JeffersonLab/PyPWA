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
from PyPWA.core.configurator.storage import module_fetcher
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


@pytest.fixture()
def module_picking():
    return module_fetcher.ModulePicking()


def test_module_picking_can_find_builtin_parser(module_picking):
    found_plugin = module_picking.request_plugin_by_name("Builtin Parser")
    assert found_plugin is not None


def test_module_picking_can_find_shell_fitting_method(module_picking):
    found_plugin = module_picking.request_main_by_id("shell fitting method")
    assert found_plugin is not None

