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

import io
import os

import numpy
import pytest
from PyPWA.builtin_plugins.data import _plugin_finder
from PyPWA.builtin_plugins.data import exceptions
from PyPWA.builtin_plugins.data.builtin import sv, gamp

CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/sv_test_data.csv"
)

GAMP_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/gamp_test_data.gamp"
)

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/temporary_write_data"
)

NOISE_LOCATION = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/noise_test_data"
)


@pytest.fixture(scope="module")
def plugin_search():
    searcher = _plugin_finder.PluginSearch()

    yield searcher


@pytest.fixture(scope="function")
def make_noise():
    with io.open(TEMP_WRITE_LOCATION, "w") as stream:
        stream.write(u"Random nonsense that isn't data.")

    yield True

    os.remove(TEMP_WRITE_LOCATION)


@pytest.fixture(scope="module")
def random_numpy_gamp_data():
    return numpy.random.rand(30, 4, 6)


@pytest.fixture(scope="module")
def random_numpy_noise():
    return numpy.random.rand(4, 4, 4, 4)


@pytest.fixture(scope="module")
def random_numpy_flat_data():
    data = numpy.zeros(30, [("x", "f8"), ("y", "f8")])
    for column in data.dtype.names:
        data[column] = numpy.random.rand(30)

    return data


def test_plugin_read_search_finds_csv_reader(plugin_search):
    """"
    Args:
        plugin_search (_plugin_finder.PluginSearch)
    """
    found = plugin_search.get_read_plugin(CSV_TEST_DATA)
    assert isinstance(found, sv.SvDataPlugin)


def test_plugin_read_search_finds_gamp_reader(plugin_search):
    """"
    Args:
        plugin_search (_plugin_finder.PluginSearch)
    """
    found = plugin_search.get_read_plugin(GAMP_TEST_DATA)
    assert isinstance(found, gamp.GampDataPlugin)


def test_plugin_read_search_finds_noise(plugin_search, make_noise):
    """"
    Args:
        plugin_search (_plugin_finder.PluginSearch)
    """
    with pytest.raises(exceptions.UnknownData):
        plugin_search.get_read_plugin(NOISE_LOCATION)


def test_plugin_write_search_finds_csv(plugin_search, random_numpy_flat_data):
    """"
    Args:
        plugin_search (_plugin_finder.PluginSearch)
        random_numpy_flat_data (numpy.ndarray)
    """
    print(len(random_numpy_flat_data.shape))
    found = plugin_search.get_write_plugin(
        CSV_TEST_DATA, random_numpy_flat_data
    )

    assert isinstance(found, sv.SvDataPlugin)


def test_plugin_write_search_finds_gamp(plugin_search, random_numpy_gamp_data):
    """"
    Args:
        plugin_search (_plugin_finder.PluginSearch)
        random_numpy_gamp_data (numpy.ndarray)
    """
    found = plugin_search.get_write_plugin(
        GAMP_TEST_DATA, random_numpy_gamp_data
    )
    print(type(found))
    assert isinstance(found, gamp.GampDataPlugin)


def test_plugin_write_search_finds_something_with_no_extension(
        plugin_search, random_numpy_flat_data
):
    """
    Args:
        plugin_search (_plugin_finder.PluginSearch)
        random_numpy_noise (numpy.ndarray)
    """
    found = plugin_search.get_write_plugin(
        TEMP_WRITE_LOCATION, random_numpy_flat_data
    )

    assert found.plugin_supports_flat_data


def test_plugin_write_search_finds_noise(plugin_search, random_numpy_noise):
    """
    Args:
        plugin_search (_plugin_finder.PluginSearch)
        random_numpy_noise (numpy.ndarray)
    """
    with pytest.raises(exceptions.UnknownData):
        plugin_search.get_write_plugin(TEMP_WRITE_LOCATION, random_numpy_noise)


def test_plugin_write_search_finds_unknown_extension(
        plugin_search, random_numpy_flat_data
):
    """"
    Args:
        plugin_search (_plugin_finder.PluginSearch)
        random_numpy_flat_data (numpy.ndarray)
    """
    location = TEMP_WRITE_LOCATION + ".completely_useless_extension"

    with pytest.raises(exceptions.UnknownData):
        plugin_search.get_write_plugin(location, random_numpy_flat_data)
