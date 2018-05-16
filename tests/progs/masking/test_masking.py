import sys

import pytest
import uuid

from PyPWA import Path
from PyPWA.entries import arguments
from PyPWA.libs import misc_file_libs, configuration_db

"""
Masking Data
"""

ROOT = Path(__file__).parent
INPUT = ROOT / "../../test_data/docs/sv_test_data.csv"
PF = ROOT / "../../test_data/docs/sv_test_data.pf"
PF2 = ROOT / "../../test_data/docs/sv_test_data2.pf"
PF_SHORT = ROOT / "../../test_data/docs/sv_test_data_short.pf"
PF_LONG = ROOT / "../../test_data/docs/sv_test_data_long.pf"
TEMP_FILE = ROOT / (
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
    if TEMP_FILE.exists():
        TEMP_FILE.unlink()


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
    [
        "pymask",
        "--input", str(INPUT),
        "-o", str(TEMP_FILE)
    ],
    [
        "pymask",
        "-i", str(INPUT),
        "--mask", str(PF),
        "-m", str(PF2),
        "-o", str(TEMP_FILE)
    ]
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
            "-i", str(INPUT),
            "--mask", str(PF),
            "-m", str(PF2),
            "-o", str(TEMP_FILE)
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
            "-i", str(INPUT),
            "--mask", str(PF),
            "-m", str(PF2),
            "--or-masks", "-o", str(TEMP_FILE)
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
            "-i", str(INPUT),
            "--mask", str(PF),
            "-m", str(PF2),
            "--xor-masks", "-o", str(TEMP_FILE)
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
        [
            "pymask",
            "-i", str(INPUT),
            "--mask", str(PF_LONG),
            "-o", str(TEMP_FILE)
        ]
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
        [
            "pymask",
            "-i", str(INPUT),
            "--mask", str(PF_SHORT),
            "-o", str(TEMP_FILE)
        ]
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
            "-i", str(INPUT),
            "--mask", str(PF),
            "--or-masks", "--xor-masks", "-o", str(TEMP_FILE)
        ]
    )


def test_masking_crash_with_or_and_xor(patch_args_critical_or_and_xor):
    with pytest.raises(ValueError):
        arguments.masking_utility()
