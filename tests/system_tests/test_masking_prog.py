from PyPWA.progs import masking
from pathlib import Path


def test_masking_errors_with_too_many_flags():
    result = masking.start_masking(
        [
            "--use_or", "--use_xor",
            "-i", "tests/test_data/docs/large.gamp",
            "-m", "tests/test_data/docs/set2.pf",
            "-o", "error_masked.gamp"
        ]
    )
    assert result == 1
    Path("error_masked.gamp").unlink(True)


def test_masking_errors_with_unmatching_data():
    result = masking.start_masking(
        [
            "-i", "tests/test_data/docs/large.gamp",
            "-m", "tests/test_data/docs/set2.pf",
            "-o", "error_masked.gamp"
        ]
    )
    assert result == 1
    Path("error_masked.gamp").unlink(True)


def test_can_mask_data():
    result = masking.start_masking(
        [
            "-i", "tests/test_data/docs/large.gamp",
            "-m", "tests/test_data/docs/set1.pf",
            "-o", "masked.gamp"
        ]
    )
    assert result != 1
    Path("masked.gamp").unlink()
