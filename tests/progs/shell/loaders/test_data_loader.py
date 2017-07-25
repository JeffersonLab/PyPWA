import os

import numpy
import pytest

from PyPWA.builtin_plugins.data import memory
from PyPWA.progs.shell import loaders


"""
Setup Data Locations
"""

# Single File data
DATA = os.path.join(
    os.path.dirname(__file__), "../../../data/shell/data/data.csv"
)

QFACTOR = os.path.join(
    os.path.dirname(__file__), "../../../data/shell/data/qfactor.txt"
)

MONTE_CARLO = os.path.join(
    os.path.dirname(__file__), "../../../data/shell/data/monte_carlo.csv"
)

# Data with embedded internal names
INTERNAL_NAMES = os.path.join(
    os.path.dirname(__file__), "../../../data/shell/data/internal_names.csv"
)

INTERNAL_NAMES_DICT = {
    "quality factor": "qf",
    "binned data": "bn",
    "event errors": "err",
    "expected values": "exp"
}

# Parser
PARSER = memory.Memory(False, True)


"""
Tests with QFactor file
"""

@pytest.fixture
def data_with_qfactor():
    loader = loaders.DataLoading(
        PARSER, DATA, qfactor=QFACTOR, monte_carlo=MONTE_CARLO
    )
    return loader


def test_qfactor_sum_file(data_with_qfactor):
    assert numpy.sum(data_with_qfactor.qfactor) == 10.794689011836818


"""
Tests without QFactor file
"""

@pytest.fixture
def data_without_qfactor():
    loader = loaders.DataLoading(
        PARSER, DATA, monte_carlo=MONTE_CARLO,
        internal_data={'quality factor': 'qfactor'}
    )
    return loader


def test_qfactor_sum_embedded(data_without_qfactor):
    assert numpy.sum(data_without_qfactor.qfactor) == 9.1540205293413841


def test_extras_not_in_data(data_without_qfactor):
    assert ["qfactor, BinN"] not in data_without_qfactor.data.dtype.names


"""
Test with Simple file.
"""

@pytest.fixture
def data_without_extra():
    loader = loaders.DataLoading(PARSER, MONTE_CARLO)
    return loader


def test_qfactor_sum_ones(data_without_extra):
    assert numpy.sum(data_without_extra.qfactor) == \
           len(data_without_extra.qfactor)


def test_monte_carlo_empty(data_without_extra):
    assert not data_without_extra.monte_carlo


def test_qfactor_size_is_correct(data_without_extra):
    multiplier = data_without_extra.qfactor * data_without_extra.data['x']
    for index, value in enumerate(multiplier):
        assert value == data_without_extra.data['x'][index]


"""
Test with all internal names.
"""

@pytest.fixture
def data_with_internal_names():
    with pytest.warns(UserWarning):
        loader = loaders.DataLoading(
            PARSER, INTERNAL_NAMES, INTERNAL_NAMES_DICT
        )
    return loader


def test_qfactor_sum_with_internal_names(data_with_internal_names):
    qfactor_sum = numpy.sum(data_with_internal_names.qfactor)
    numpy.testing.assert_approx_equal(qfactor_sum, 3.5613567269141941)


def test_binned_sum_with_internal_names(data_with_internal_names):
    assert numpy.sum(data_with_internal_names.binned) == 4.1548651531099434


def test_error_sum_with_internal_names(data_with_internal_names):
    error_sum = numpy.sum(data_with_internal_names.event_errors)
    numpy.testing.assert_approx_equal(error_sum, 4.088662060902655)


def test_expected_sum_with_internal_names(data_with_internal_names):
    assert numpy.sum(data_with_internal_names.expected_values) == \
           4.7432790009769166


def test_length_of_all_data_match_with_internal(data_with_internal_names):
    data_len = len(data_with_internal_names.data)
    qfactor_len = len(data_with_internal_names.data)
    binned_len = len(data_with_internal_names.data)
    measurement_len = len(data_with_internal_names.data)
    errors_len = len(data_with_internal_names.data)
    data = [data_len, qfactor_len, binned_len, measurement_len, errors_len]
    assert len(set(data)) == 1
