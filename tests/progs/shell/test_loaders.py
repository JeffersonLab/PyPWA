import os

import numpy
import pytest

from PyPWA.builtin_plugins.data import memory
from PyPWA.progs.shell import loaders

DATA = os.path.join(
    os.path.dirname(__file__), "../../data/shell/data/data.csv"
)

INTERNAL_NAMES = os.path.join(
    os.path.dirname(__file__), "../../data/shell/data/internal_names.csv"
)

INTERNAL_NAMES_DICT = {
    "quality factor": "qf",
    "binned data": "bn",
    "event errors": "err",
    "expected values": "exp"
}

QFACTOR = os.path.join(
    os.path.dirname(__file__), "../../data/shell/data/qfactor.txt"
)

MONTE_CARLO = os.path.join(
    os.path.dirname(__file__), "../../data/shell/data/monte_carlo.csv"
)

PARSER = memory.Memory(False, True)

FUNCTIONS_FOR_TEST = os.path.join(
    os.path.dirname(__file__),
    "../../data/source_files/functions_without_math.py"
)


@pytest.fixture
def data_with_qfactor():
    loader = loaders.DataLoading(
        PARSER, DATA, qfactor=QFACTOR, monte_carlo=MONTE_CARLO
    )
    return loader


@pytest.fixture
def data_without_qfactor():
    loader = loaders.DataLoading(PARSER, DATA, monte_carlo=MONTE_CARLO)
    return loader


@pytest.fixture
def data_without_extra():
    loader = loaders.DataLoading(PARSER, MONTE_CARLO)
    return loader


@pytest.fixture
def data_with_internal_names():
    loader = loaders.DataLoading(PARSER, INTERNAL_NAMES, INTERNAL_NAMES_DICT)
    return loader


def test_qfactor_sum_embedded(data_without_qfactor):
    assert numpy.sum(data_without_qfactor.qfactor) == 9.1540205293413841


def test_qfactor_sum_file(data_with_qfactor):
    assert numpy.sum(data_with_qfactor.qfactor) == 10.794689011836818


def test_qfactor_sum_ones(data_without_extra):
    assert numpy.sum(data_without_extra.qfactor) == \
           len(data_without_extra.qfactor)


def test_monte_carlo_empty(data_without_extra):
    assert not data_without_extra.monte_carlo


def test_extras_not_in_data(data_without_qfactor):
    assert ["qfactor, BinN"] not in data_without_qfactor.data.dtype.names


def test_qfactor_size_is_correct(data_without_extra):
    multiplier = data_without_extra.qfactor * data_without_extra.data['x']
    for index, value in enumerate(multiplier):
        assert value == data_without_extra.data['x'][index]


def test_qfactor_sum_with_internal_names(data_with_internal_names):
    assert numpy.sum(data_with_internal_names.qfactor) == 4.3227260998520247


def test_binned_sum_with_internal_names(data_with_internal_names):
    assert numpy.sum(data_with_internal_names.binned) == 4.7429487930395018


def test_error_sum_with_internal_names(data_with_internal_names):
    numpy.testing.assert_approx_equal(
        numpy.sum(data_with_internal_names.event_errors),
        4.2857024214064667
    )


def test_expected_sum_with_internal_names(data_with_internal_names):
    assert numpy.sum(data_with_internal_names.expected_values) == \
           5.673049557244684


@pytest.fixture
def function_without_math():
    loader = loaders.FunctionLoader(
        FUNCTIONS_FOR_TEST, "processing", "setup"
    )
    return loader


@pytest.fixture
def function_without_math_or_setup():
    loader = loaders.FunctionLoader(
        FUNCTIONS_FOR_TEST, "processing", "A dirty lie"
    )
    return loader


def test_function_and_setup_return_true(function_without_math):
    processing = function_without_math.process
    setup = function_without_math.setup
    assert processing(1, 1)
    assert setup()


def test_function_without_setup_is_none(function_without_math_or_setup):
    setup = function_without_math_or_setup.setup
    assert isinstance(setup(), type(None))
