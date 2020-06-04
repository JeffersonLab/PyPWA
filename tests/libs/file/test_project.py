# coding=utf-8

from pathlib import Path

import pandas.testing
import pytest

from PyPWA.libs import vectors
from PyPWA.libs.file import project, processor

HDF = Path("./project_test.hd5")
DATA_DIR = (Path(__file__).parent / "../../test_data/docs").resolve()
GAMP_DATA = DATA_DIR / "large.gamp"
REGULAR_DATA = DATA_DIR / "set1.csv"
REGULAR_PF = DATA_DIR / "set1.pf"
REGULAR_QF = DATA_DIR / "set1.txt"


@pytest.fixture(scope="module")
def parser():
    return processor.DataProcessor(False, False)


@pytest.fixture(scope="module")
def project_manager(parser):
    manager = project.ProjectDatabase(HDF, "w")
    manager.make_folder(
        "gamp", parser.get_reader(GAMP_DATA), "events.gamp", True
    )

    data_folder = manager.make_folder(
        "data", parser.parse(REGULAR_DATA), "other_events.gamp", False
    )

    data_folder.data.add_data(
        data_folder.data.Data.PASSFAIL, parser.parse(REGULAR_PF)
    )
    data_folder.data.add_data(
        data_folder.data.Data.QFACTOR, parser.parse(REGULAR_QF)
    )

    yield manager

    manager.close()
    HDF.unlink()


def test_gamp_data_matches(parser, project_manager):
    gamp_folder = project_manager.get_folder("gamp")
    folder_root_data = gamp_folder.root.data.read()

    expected_data = parser.parse(GAMP_DATA)

    zipped_particles = zip(
        folder_root_data.iter_particles(), expected_data.iter_particles()
    )

    for parsed, expected in zipped_particles:  # type: vectors.Particle
        assert parsed.id == expected.id
        pandas.testing.assert_frame_equal(parsed.dataframe, expected.dataframe)


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_binning_fixed_count(project_manager):
    gamp_folder = project_manager.get_folder("gamp")
    gamp_folder.binning.add_fixed_count(project.BinVars.T, 3)
    gamp_folder.binning.execute()

    directory = gamp_folder.binning.get_bin_directory()

    total_sum = 0
    for folder in directory:
        total_sum += len(folder)

    assert len(gamp_folder) == total_sum


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_binning_width(project_manager):
    gamp_folder = project_manager.get_folder("gamp")
    gamp_folder.binning.add_fixed_range(
        project.BinVars.MASS, .59, .9, 4
    )
    gamp_folder.binning.execute()

    directory = gamp_folder.binning.get_bin_directory()

    total_sum = 0
    for folder in directory:
        total_sum += len(folder)

    assert len(gamp_folder) == total_sum


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_binning_combined(project_manager):
    gamp_folder = project_manager.get_folder("gamp")
    gamp_folder.binning.add_fixed_count(project.BinVars.T, 3)
    gamp_folder.binning.add_fixed_range(
        project.BinVars.MASS, .59, .9, 4
    )
    gamp_folder.binning.execute()

    directory = gamp_folder.binning.get_bin_directory()

    total_sum = 0
    for folder in directory:
        total_sum += len(folder)

    assert len(gamp_folder) == total_sum
