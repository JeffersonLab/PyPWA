import os

import numpy
import pytest

from PyPWA.builtin_plugins.data import memory
from PyPWA.shell import loaders

DATA = os.path.join(
    os.path.dirname(__file__), "../data/data.csv"
)

QFACTOR = os.path.join(
    os.path.dirname(__file__), "../data/qfactor.txt"
)

MONTE_CARLO = os.path.join(
    os.path.dirname(__file__), "../data/monte_carlo.csv"
)

PARSER = memory.Memory(False, True)

FUNCTIONS_FOR_TEST = os.path.join(
    os.path.dirname(__file__), "../data/functions_without_math.py"
)


@pytest.fixture
def data_with_qfactor():
    loader = loaders.DataLoading(PARSER, DATA, QFACTOR, MONTE_CARLO)
    loader.load_data()
    return loader


@pytest.fixture
def data_without_qfactor():
    loader = loaders.DataLoading(PARSER, DATA, monte_carlo=MONTE_CARLO)
    loader.load_data()
    return loader


@pytest.fixture
def data_without_extra():
    loader = loaders.DataLoading(PARSER, MONTE_CARLO)
    loader.load_data()
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


@pytest.fixture
def function_without_math():
    loader = loaders.FunctionLoader(
        FUNCTIONS_FOR_TEST, "processing", "setup"
    )
    loader.load_functions()
    return loader


@pytest.fixture
def function_without_math_or_setup():
    loader = loaders.FunctionLoader(
        FUNCTIONS_FOR_TEST, "processing", "A dirty lie"
    )
    loader.load_functions()
    return loader


def test_function_and_setup_return_true(function_without_math):
    processing = function_without_math.process
    setup = function_without_math.setup
    assert processing(1, 1)
    assert setup()


def test_function_without_setup_is_none(function_without_math_or_setup):
    setup = function_without_math_or_setup.setup
    assert isinstance(setup(), type(None))
