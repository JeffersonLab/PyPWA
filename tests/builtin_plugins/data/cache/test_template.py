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
from PyPWA.builtin_plugins.data.cache import _template


@pytest.fixture
def writer():
    return _template.WriteInterface()


@pytest.fixture
def reader():
    return _template.ReadInterface()


def test_write_interface_write_cache(writer):
    with pytest.raises(NotImplementedError):
        writer.write_cache("123")


def test_read_interface_is_valid(reader):
    with pytest.raises(NotImplementedError):
        reader.is_valid


def test_read_interface_get_cache(reader):
    with pytest.raises(NotImplementedError):
        reader.get_cache()
