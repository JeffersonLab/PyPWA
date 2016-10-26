import os

import pytest
from PyPWA.builtin_plugins.data import exceptions
from PyPWA.builtin_plugins.data.builtin.sv import read_tests

CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../test_docs/sv_test_data.csv"
)

TSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../test_docs/sv_test_data.tsv"
)

BAD_CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../test_docs/sv_test_data_bad.csv"
)

NOISE_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../test_docs/noise_test_data"
)


@pytest.fixture(scope="module")
def setup_test():
    """
    Returns:
        data_templates.ReadTest
    """
    return read_tests.SvDataTest()


@pytest.fixture(scope="module", params=[NOISE_TEST_DATA, BAD_CSV_TEST_DATA])
def tests_fails(request):
    return request.param


@pytest.fixture(scope="module", params=[CSV_TEST_DATA, TSV_TEST_DATA])
def tests_passes(request):
    return request.param


def test_quick_test_fails_with_bad_files(setup_test, tests_fails):
    """
    Args:
        setup_test (data_templates.ReadTest)
        tests_fails (str)
    """
    with pytest.raises(exceptions.IncompatibleData):
        setup_test.quick_test(tests_fails)


def test_full_test_fails_with_bad_files(setup_test, tests_fails):
    """
    Args:
        setup_test (data_templates.ReadTest)
        tests_fails (str)
    """
    with pytest.raises(exceptions.IncompatibleData):
        setup_test.full_test(tests_fails)


def test_quick_test_passes_with_good_files(setup_test, tests_passes):
    """
    Args:
        setup_test (data_templates.ReadTest)
        tests_passes (str)
    """
    setup_test.quick_test(tests_passes)


def test_full_test_passes_with_good_files(setup_test, tests_passes):
    """
    Args:
        setup_test (data_templates.ReadTest)
        tests_passes (str)
    """
    setup_test.full_test(tests_passes)
