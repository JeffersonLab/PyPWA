from pathlib import Path

import pytest

from PyPWA.plugins.data import pgz

ROOT = (Path(__file__).parent / "../../test_data/docs").resolve()

TEMP_LOCATION = ROOT / "temporary_write_data.pgz"


@pytest.fixture
def parser():
    return pgz.metadata.get_memory_parser()


def test_parser_and_writer(parser, structured_data, check_memory_read_write):
    check_memory_read_write(parser, structured_data, TEMP_LOCATION)
