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

import sys
import pytest
from PyPWA import Path
from PyPWA.libs.components.data_processor.cache import _clear_cache
from PyPWA.libs.components.data_processor.cache import _basic_info


class BasicTestInfo(_basic_info.FindBasicInfo):

    def __init__(self):
        # We don't actually want to run the init
        pass

    @property
    def file_hash(self):
        return "1234567890aoeuidhtns"

    @property
    def cache_location(self):
        return Path("narnia")


@pytest.fixture
def mock_os_remove_no_file(monkeypatch):
    def raise_oserror(location):
        raise OSError

    if sys.version_info[0:2] >= (3,4):
        monkeypatch.setattr(
            "pathlib.Path.unlink",
            raise_oserror
        )
    else:
        monkeypatch.setattr(
            "pathlib2.Path.unlink",
            raise_oserror
        )


@pytest.fixture
def mock_os_remove_no_error(monkeypatch):
    def no_error(location):
        pass

    if sys.version_info[0:2] >= (3,4):
        monkeypatch.setattr(
            "pathlib.Path.unlink",
            no_error
        )
    else:
        monkeypatch.setattr(
            "pathlib2.Path.unlink",
            no_error
        )



@pytest.fixture
def setup_test_info():
    return BasicTestInfo()


@pytest.fixture
def clear_cache_with_success(setup_test_info, mock_os_remove_no_error):
    return _clear_cache.ClearCache(setup_test_info)


@pytest.fixture
def clear_cache_without_success(setup_test_info, mock_os_remove_no_file):
    return _clear_cache.ClearCache(setup_test_info)


def test_is_valid_is_false(clear_cache_with_success):
    assert not clear_cache_with_success.is_valid()


def test_get_cache_raises_error(clear_cache_without_success):
    with pytest.raises(RuntimeError):
        clear_cache_without_success.get_cache()
