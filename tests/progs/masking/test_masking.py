import os
import sys
import uuid

import pytest

from PyPWA.entries import arguments
from PyPWA.libs import misc_file_libs, configuration_db

"""
Masking Data
"""

INPUT = os.path.join(
    os.path.dirname(__file__), "../../test_data/docs/sv_test_data.csv"
)

PF = os.path.join(
    os.path.dirname(__file__), "../../test_data/docs/sv_test_data.pf"
)

PF2 = os.path.join(
    os.path.dirname(__file__), "../../test_data/docs/sv_test_data2.pf"
)

PF_SHORT = os.path.join(
    os.path.dirname(__file__), "../../test_data/docs/sv_test_data_short.pf"
)

PF_LONG = os.path.join(
    os.path.dirname(__file__), "../../test_data/docs/sv_test_data_long.pf"
)

TEMP_FILE = os.path.join(
    os.path.dirname(__file__),
    "../../test_data/docs/temp_" + str(uuid.uuid4()) + "_file.txt"
)


"""
Helping functions
"""

@pytest.fixture()
def correct_argv(monkeypatch):
    original = sys.argv
    yield
    monkeypatch.setattr("sys.argv", original)


@pytest.fixture()
def cleanup_temp():
    yield
    os.remove(TEMP_FILE)


@pytest.fixture()
def clear_settings():
    settings = configuration_db.Connector()
    yield
    with pytest.warns(RuntimeWarning):
        settings.purge()

"""
Test Masking can run without crashing
"""

tested_args = [
    ["pymask", "--input", INPUT, "-o", TEMP_FILE],
    ["pymask", "-i", INPUT, "--mask", PF, "-m", PF2, "-o", TEMP_FILE]
]
@pytest.fixture(params=tested_args)
def patch_args_clean(
        monkeypatch, request, correct_argv, cleanup_temp, clear_settings
):
    monkeypatch.setattr("sys.argv", request.param)


def test_masking_utility(patch_args_clean):
    arguments.masking_utility()


"""
Test Masking with multiple masks has the correct number of lines
"""

@pytest.fixture()
def patch_args_double_mask(
        monkeypatch, request, correct_argv, cleanup_temp, clear_settings
):
    monkeypatch.setattr(
        "sys.argv",
        [
            "pymask",
            "-i", INPUT, "--mask", PF, "-m", PF2, "-o", TEMP_FILE
        ]
    )
    arguments.masking_utility()
    yield


def test_masking_utility_has_correct_number_of_lines(patch_args_double_mask):
    assert misc_file_libs.get_file_length(TEMP_FILE) == 1


"""
Test Masking with multiple OR masks has the correct number of lines
"""

@pytest.fixture()
def patch_args_double_mask_or(
        monkeypatch, request, correct_argv, cleanup_temp, clear_settings
):
    monkeypatch.setattr(
        "sys.argv",
        [
            "pymask",
            "-i", INPUT, "--mask", PF, "-m", PF2, "--or-masks", "-o",
            TEMP_FILE
        ]
    )
    arguments.masking_utility()
    yield


def test_masking_or(patch_args_double_mask_or):
    assert misc_file_libs.get_file_length(TEMP_FILE) == 3


"""
Test Masking with multiple XOR masks has the correct number of lines
"""

@pytest.fixture()
def patch_args_double_mask_xor(
        monkeypatch, request, correct_argv, cleanup_temp, clear_settings
):
    monkeypatch.setattr(
        "sys.argv",
        [
            "pymask",
            "-i", INPUT, "--mask", PF, "-m", PF2, "--xor-masks", "-o",
            TEMP_FILE
        ]
    )
    arguments.masking_utility()
    yield


def test_masking_xor(patch_args_double_mask_xor):
    assert misc_file_libs.get_file_length(TEMP_FILE) == 2


"""
Test Masking with more masked events than data
"""

@pytest.fixture()
def patch_args_warning(
        monkeypatch, correct_argv, cleanup_temp, clear_settings
):
    monkeypatch.setattr(
        "sys.argv",
        ["pymask", "-i", INPUT, "--mask", PF_LONG, "-o", TEMP_FILE]
    )


def test_masking_warning(patch_args_warning):
    with pytest.warns(UserWarning):
        arguments.masking_utility()


"""
Test Masking with less masked events than data
"""

@pytest.fixture()
def patch_args_critical(
        monkeypatch, correct_argv, cleanup_temp, clear_settings
):
    monkeypatch.setattr(
        "sys.argv",
        ["pymask", "-i", INPUT, "--mask", PF_SHORT, "-o", TEMP_FILE]
    )


def test_masking_crash(patch_args_critical):
    with pytest.raises(IndexError):
        arguments.masking_utility()


"""
Test Masking with both OR and XOR
"""

@pytest.fixture()
def patch_args_critical_or_and_xor(monkeypatch, correct_argv, clear_settings):
    monkeypatch.setattr(
        "sys.argv",
        [
            "pymask",
            "-i", INPUT,
            "--mask", PF, "--or-masks", "--xor-masks",
            "-o", TEMP_FILE
        ]
    )


def test_masking_crash_with_or_and_xor(patch_args_critical_or_and_xor):
    with pytest.raises(ValueError):
        arguments.masking_utility()
