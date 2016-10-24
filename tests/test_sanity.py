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


@pytest.mark.xfail(reason="Empty files should have no lines.")
def test_empty_file_has_lines(io_open):
    """
    Args:
        io_open (io.FileIO)
    """
    print("\nPytest runs xfail functions!\n")
    assert len(io_open.readlines()) > 1


@pytest.fixture
def os_remove_equals_3(monkeypatch):
    def returns_3(*args):
        # We don't actually care about the arguments
        return 3

    monkeypatch.setattr("os.remove", returns_3)


def test_os_remove_returns_3(os_remove_equals_3):
    assert os.remove("A random path.") == 3
