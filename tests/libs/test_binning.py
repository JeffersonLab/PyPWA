#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016 JLab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as npy
import pandas as pd
import pytest

from PyPWA.libs import binning


"""
Fixtures for Binning Tests
"""

@pytest.fixture()
def dataframe():
    df = pd.DataFrame()
    df['x'] = npy.random.rand(10_000)
    df['y'] = npy.random.rand(10_000)
    df['z'] = npy.random.rand(10_000)

    return df


@pytest.fixture()
def array():
    array = npy.empty(10_000, [('x', 'f8'), ('y', 'f8'), ('z', 'f8')])
    array['x'] = npy.random.rand(10_000)
    array['y'] = npy.random.rand(10_000)
    array['z'] = npy.random.rand(10_000)

    return array


@pytest.fixture(params=["dataframe", "structured"])
def data(request, dataframe, array):
    if request.param == "dataframe":
        return dataframe
    elif request.param == "structured":
        return array
    else:
        assert "datatype is not set as expected!"


"""
Tests for the bin_by_range function
"""


def test_range_throws_error(array):
    wrong_size = npy.random.rand(15_000)
    with pytest.raises(ValueError):
        binning.bin_by_range(array, wrong_size, 10)


def test_bin_by_range_trims_data(data):
    results = binning.bin_by_range(
        data, 'x', 10, lower_cut=0.1, upper_cut=0.9
    )
    for result in results:
        assert npy.all(result['x'] >= 0.1)
        assert npy.all(result['x'] <= 0.9)


def test_range_correct_number_of_bins(data):
    results = binning.bin_by_range(data, 'x', 10)
    assert len(results) == 10


def test_range_sample_size_reduces_data_size(data):
    results = binning.bin_by_range(data, 'x', 10, sample_size=100)
    assert npy.sum([len(x) for x in results]) == 1000


def test_sum_of_all_range_lengths_matches_original(data):
    results = binning.bin_by_range(data, 'x', 10)
    assert npy.sum([len(x) for x in results]) == len(data)


"""
Tests for the bin_with_fixed_widths function
"""


def test_fixed_widths_throws_error(array):
    wrong_size = npy.random.rand(15_000)
    with pytest.raises(ValueError):
        binning.bin_with_fixed_widths(array, wrong_size, 10)


def test_fixed_widths_returns_expected_number_of_bins(data):
    results = binning.bin_with_fixed_widths(data, 'x', 1000)
    assert len(results) == 10


def test_fixed_widths_handles_bin_overflows(data):
    results = binning.bin_with_fixed_widths(data, 'x', 900)
    # Check first and last element of results has length of 50
    assert len(results[0]) == 50
    assert len(results[-1]) == 50

    # Check that the rest of the bins have length of 900
    for result in results[1:-1]:
        assert len(result) == 900


"""
Finally, test bin_by_lists
"""

