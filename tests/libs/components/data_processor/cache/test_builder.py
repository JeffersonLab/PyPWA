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
from PyPWA.libs.components.data_processor.cache import _template
from PyPWA.libs.components.data_processor.cache import builder


##############################################################################
# Cache Test Overrides
##############################################################################

class DidNotWrite(Exception):
    pass


class DidWrite(Exception):
    pass


class DidRead(Exception):
    pass


class DidNotRead(Exception):
    pass


class ReadCleared(Exception):
    pass


class NoWriteTest(_template.WriteInterface):

    def write_cache(self, data):
        raise DidNotWrite


class NoReadTest(_template.ReadInterface):

    @property
    def is_valid(self):
        raise DidNotRead

    def get_cache(self):
        raise DidNotRead


class WriteTest(_template.WriteInterface):

    def __init__(self, info):
        pass

    def write_cache(self, data):
        raise DidWrite


class ReadTest(_template.ReadInterface):

    def __init__(self, info):
        pass

    @property
    def is_valid(self):
        raise DidRead

    def get_cache(self):
        raise DidRead


class ReadClearTest(_template.ReadInterface):

    def __init__(self, info):
        pass

    @property
    def is_valid(self):
        raise ReadCleared

    def get_cache(self):
        raise ReadCleared


class MockBasicInfo(object):

    def setup_basic_info(self, original_file):
        pass

    @property
    def file_hash(self):
        return "1234567890aoeuidhtns"

    @property
    def cache_location(self):
        return "A location"


class MockBasicInfoNoFile(object):

    def setup_basic_info(self, original_file):
        pass

    @property
    def file_hash(self):
        return None

    @property
    def cache_location(self):
        return ""


##############################################################################
# Mocking for Cache
##############################################################################

@pytest.fixture
def mock_no_cache(monkeypatch):
    monkeypatch.setattr(
        "PyPWA.libs.components.data_processor.cache._no_cache.NoWrite",
        NoWriteTest
    )

    monkeypatch.setattr(
        "PyPWA.libs.components.data_processor.cache._no_cache.NoRead",
        NoReadTest
    )


@pytest.fixture
def mock_standard_cache(monkeypatch):
    monkeypatch.setattr(
        "PyPWA.libs.components.data_processor.cache._standard_cache.WriteCache",
        WriteTest
    )

    monkeypatch.setattr(
        "PyPWA.libs.components.data_processor.cache._standard_cache.ReadCache",
        ReadTest
    )


@pytest.fixture
def mock_clear_cache(monkeypatch):
    monkeypatch.setattr(
        "PyPWA.libs.components.data_processor.cache._clear_cache.ClearCache",
        ReadClearTest
    )


@pytest.fixture
def mock_basic_info(monkeypatch):
    monkeypatch.setattr(
        "PyPWA.libs.components.data_processor.cache._basic_info.FindBasicInfo",
        MockBasicInfo
    )


@pytest.fixture
def mock_basic_info_no_file(monkeypatch):
    monkeypatch.setattr(
        "PyPWA.libs.components.data_processor.cache._basic_info.FindBasicInfo",
        MockBasicInfoNoFile
    )


##############################################################################
# Fixtures for tests
##############################################################################

@pytest.fixture
def interface_with_cache_and_noclear(
        mock_no_cache, mock_standard_cache, mock_clear_cache,
        mock_basic_info,
):
    build = builder.CacheBuilder(True, False)
    return build.get_cache_interface("a file location")


@pytest.fixture
def interface_with_cache_and_clear(
        mock_no_cache, mock_standard_cache, mock_clear_cache,
        mock_basic_info
):
    build = builder.CacheBuilder(True, True)
    return build.get_cache_interface("a file location")


@pytest.fixture
def interface_with_nocache(
        mock_no_cache, mock_standard_cache, mock_clear_cache,
        mock_basic_info
):
    build = builder.CacheBuilder(False, False)
    return build.get_cache_interface("a file location")


##############################################################################
# Cache tests
##############################################################################

@pytest.fixture(params=[0, 1, 2])
def param_wrapper(
        request, interface_with_cache_and_noclear,
        interface_with_cache_and_clear, interface_with_nocache
):
    if request.param == 0:
        return [
            interface_with_cache_and_noclear,
            {"write": DidWrite, "read": DidRead, "valid": DidRead},
            "Cache True, Clear False"
        ]
    elif request.param == 1:
        return [
            interface_with_cache_and_clear,
            {"write": DidWrite, "read": ReadCleared, "valid": ReadCleared},
            "Cache True, Clear True"
        ]
    elif request.param == 2:
        return [
            interface_with_nocache,
            {"write": DidNotWrite, "read": DidNotRead, "valid": DidNotRead},
            "Cache False, Clear False"
        ]


def test_write_cache(param_wrapper):
    with pytest.raises(param_wrapper[1]["write"]):
        param_wrapper[0].write_cache("123")


def test_read_cache(param_wrapper):
    with pytest.raises(param_wrapper[1]["read"]):
        param_wrapper[0].read_cache()


def test_cache_is_valid(param_wrapper):
    with pytest.raises(param_wrapper[1]["valid"]):
        param_wrapper[0].is_valid()


@pytest.fixture
def cache_with_no_file(
        mock_no_cache, mock_standard_cache, mock_clear_cache,
        mock_basic_info_no_file
):
    build = builder.CacheBuilder(True, False)
    return build.get_cache_interface("A File")


def test_cache_is_not_valid_when_no_file(cache_with_no_file):
    with pytest.raises(DidNotRead):
        cache_with_no_file.is_valid()
