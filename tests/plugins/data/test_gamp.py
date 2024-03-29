from pathlib import Path

import pytest

from PyPWA.plugins.data import gamp

ROOT = (Path(__file__).parent / "../../test_data/docs").resolve()
TEMP_LOCATION = ROOT / "temporary_write_data.gamp"
LARGE = ROOT / "large.gamp"
MULTI = ROOT / "multiple.gamp"


@pytest.fixture()
def gamp_mem():
    return gamp._GampMemory()


@pytest.fixture()
def large_gamp(gamp_mem):
    return gamp_mem.parse(LARGE)


@pytest.fixture()
def multi_gamp(gamp_mem):
    return gamp_mem.parse(MULTI)


def test_large_has_all_events(large_gamp):
    assert 1000 == large_gamp.event_count


def test_multi_has_all_events(multi_gamp):
    assert 5 == multi_gamp.event_count


def test_large_has_four_particles(large_gamp):
    assert 4 == len(large_gamp)


def test_multi_has_six_particles(multi_gamp):
    assert 6 == len(multi_gamp)


def test_write_data(multi_gamp, gamp_mem):
    gamp_mem.write(TEMP_LOCATION, multi_gamp)
    intermediate = gamp_mem.parse(TEMP_LOCATION)
    TEMP_LOCATION.unlink(True)  # clear the space after it's loaded.

    assert intermediate == multi_gamp
