import sys
import os

import pytest

from PyPWA.core.arguments import start

"""
Masking Data
"""

INPUT = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/sv_test_data.csv"
)

PF = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/sv_test_data.pf"
)

PF_SHORT = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/sv_test_data_short.pf"
)

PF_LONG = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/sv_test_data_long.pf"
)

"""
Test Masking with Standard Data
"""


@pytest.fixture()
def correct_argv(monkeypatch):
    original = sys.argv
    yield
    monkeypatch.setattr("sys.argv", original)


@pytest.fixture()
def cleanup_temp():
    yield
    os.remove("testfile.txt")


tested_args = [
    ["pymask", "--input", INPUT, "-o", "testfile.txt"],
    ["pymask", "-i", INPUT, "--mask", PF, "-o", "testfile.txt"]
]
@pytest.fixture(params=tested_args)
def patch_args_clean(monkeypatch, request, correct_argv, cleanup_temp):
    monkeypatch.setattr("sys.argv", request.param)


@pytest.fixture()
def start_args(patch_args_clean):
    return start.StartArguments()


def test_masking_utility(start_args):
    start_args.start('masking utility', 'basic masking utility')


"""
Test Masking with more masked events than data
"""


@pytest.fixture()
def patch_args_warning(monkeypatch, correct_argv, cleanup_temp):
    monkeypatch.setattr(
        "sys.argv",
        ["pymask", "-i", INPUT, "--mask", PF_LONG, "-o", "testfile.txt"]
    )


@pytest.fixture()
def start_args_long(patch_args_warning):
    return start.StartArguments()


def test_masking_warning(start_args_long):
    with pytest.warns(UserWarning):
        start_args_long.start('masking utility', 'basic masking utility')


"""
Test Masking with less masked events than data
"""


@pytest.fixture()
def patch_args_critical(monkeypatch, correct_argv, cleanup_temp):
    monkeypatch.setattr(
        "sys.argv",
        ["pymask", "-i", INPUT, "--mask", PF_SHORT, "-o", "testfile.txt"]
    )


@pytest.fixture()
def start_args_short(patch_args_critical):
    return start.StartArguments()


def test_masking_crash(start_args_short):
    with pytest.raises(IndexError):
        start_args_short.start('masking utility', 'basic masking utility')
