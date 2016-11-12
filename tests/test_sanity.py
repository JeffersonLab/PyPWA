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

import pytest


@pytest.fixture(scope="module", params=[".testfile", ".anotherfile"])
def io_open(request):
    io.open(request.param, "w").close()
    opened_file = io.open(request.param)

    yield opened_file

    opened_file.close()
    os.remove(request.param)


def test_empty_file_has_no_lines(io_open):
    """
    Args:
        io_open (io.FileIO)
    """
    assert io_open.read() == ""


@pytest.mark.xfail(reason="Empty files should have no lines.", strict=True)
def test_empty_file_has_lines(io_open):
    """
    Args:
        io_open (io.FileIO)
    """
    assert len(io_open.readlines()) > 1


@pytest.fixture
def os_remove_equals_3(monkeypatch):
    def returns_3(*args):
        # We don't actually care about the arguments
        return 3

    monkeypatch.setattr("os.remove", returns_3)


def test_os_remove_returns_3(os_remove_equals_3):
    assert os.remove("A random path.") == 3


def test_error_catching_works():
    with pytest.raises(IOError):
        raise IOError
