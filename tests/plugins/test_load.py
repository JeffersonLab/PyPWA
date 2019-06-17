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

from PyPWA.plugins import data, load


@pytest.fixture
def found_data_plugins():
    return load(data, "Data Test")


def find_data_name(plugins, name):
    found = False
    for plugin in plugins:
        if plugin.plugin_name == name:
            found = True
    return found


def test_found_sv_data(found_data_plugins):
    assert find_data_name(
        found_data_plugins, "Delimiter Separated Variable sheets"
    )


def test_found_gamp_data(found_data_plugins):
    assert find_data_name(found_data_plugins, "gamp")
