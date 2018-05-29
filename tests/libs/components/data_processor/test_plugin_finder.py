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

from PyPWA import Path
from PyPWA.builtin_plugins import sv, gamp
from PyPWA.libs.components.data_processor import _plugin_finder, exceptions


"""
File Locations
"""

ROOT = Path(__file__).parent
CSV_TEST_DATA = ROOT / "../../../test_data/docs/sv_test_data.csv"
GAMP_TEST_DATA = ROOT / "../../../test_data/docs/gamp_test_data.gamp"
TEMP_WRITE_LOCATION = ROOT / "../../../test_data/docs/temporary_write_data"
NOISE_LOCATION = ROOT / "../../../test_data/docs/noise_test_data"


"""
Helping Functions
"""

@pytest.fixture(scope="module")
def plugin_search():
    searcher = _plugin_finder.PluginSearch()

    yield searcher


@pytest.fixture(scope="function")
def make_noise():
    with TEMP_WRITE_LOCATION.open("w") as stream:
        stream.write(u"Random nonsense that isn't data.")

    yield True

    TEMP_WRITE_LOCATION.unlink()


"""
Tests
"""

def test_plugin_read_search_finds_csv_reader(plugin_search):

    found = plugin_search.get_read_plugin(CSV_TEST_DATA)
    assert isinstance(found, sv.SvDataPlugin)


def test_plugin_read_search_finds_gamp_reader(plugin_search):
    found = plugin_search.get_read_plugin(GAMP_TEST_DATA)
    assert isinstance(found, gamp.GampDataPlugin)


def test_plugin_read_search_finds_noise(plugin_search):
    with pytest.raises(exceptions.UnknownData):
        plugin_search.get_read_plugin(NOISE_LOCATION)


def test_plugin_write_search_finds_csv(plugin_search):
    found = plugin_search.get_write_plugin(CSV_TEST_DATA)
    assert isinstance(found, sv.SvDataPlugin)


def test_plugin_write_search_finds_gamp(plugin_search):
    found = plugin_search.get_write_plugin(
        GAMP_TEST_DATA, is_particle_pool=True
    )
    assert isinstance(found, gamp.GampDataPlugin)


def test_plugin_write_search_finds_something_with_no_extension(plugin_search):
    found = plugin_search.get_write_plugin(
        TEMP_WRITE_LOCATION
    )
    assert found.plugin_supports_columned_data


def test_plugin_write_search_finds_unknown_extension(plugin_search):
    location = Path(
        TEMP_WRITE_LOCATION.stem + ".completely_useless_extension"
    )

    with pytest.raises(exceptions.UnknownData):
        plugin_search.get_write_plugin(location)
