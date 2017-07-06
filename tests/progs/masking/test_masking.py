import os
import sys

import pytest

from PyPWA.entries import arguments
from PyPWA.core.shared import file_libs

"""
Masking Data
"""

INPUT = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/sv_test_data.csv"
)

PF = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/sv_test_data.pf"
)

PF2 = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/sv_test_data2.pf"
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
    ["pymask", "-i", INPUT, "--mask", PF, "-m", PF2, "-o", "testfile.txt"]
]
@pytest.fixture(params=tested_args)
def patch_args_clean(monkeypatch, request, correct_argv, cleanup_temp):
    monkeypatch.setattr("sys.argv", request.param)


def test_masking_utility(patch_args_clean):
    arguments.masking_utility()


"""
Test Masking with Standard Data
"""

@pytest.fixture()
def patch_args_double_mask(monkeypatch, request, correct_argv, cleanup_temp):
    monkeypatch.setattr(
        "sys.argv",
        [
            "pymask",
            "-i", INPUT, "--mask", PF, "-m", PF2, "-o", "testfile.txt"
        ]
    )
    arguments.masking_utility()
    yield


def test_masking_utility_has_correct_number_of_lines(patch_args_double_mask):
    assert file_libs.get_file_length("testfile.txt") == 1


"""
Test Masking with more masked events than data
"""

@pytest.fixture()
def patch_args_warning(monkeypatch, correct_argv, cleanup_temp):
    monkeypatch.setattr(
        "sys.argv",
        ["pymask", "-i", INPUT, "--mask", PF_LONG, "-o", "testfile.txt"]
    )


def test_masking_warning(patch_args_warning):
    with pytest.warns(UserWarning):
        arguments.masking_utility()


"""
Test Masking with less masked events than data
"""

@pytest.fixture()
def patch_args_critical(monkeypatch, correct_argv, cleanup_temp):
    monkeypatch.setattr(
        "sys.argv",
        ["pymask", "-i", INPUT, "--mask", PF_SHORT, "-o", "testfile.txt"]
    )


def test_masking_crash(patch_args_critical):
    with pytest.raises(IndexError):
        arguments.masking_utility()
