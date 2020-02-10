#  Copyright (C) 2016  JLab
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

from pathlib import Path

import numpy as npy
import pandas
import pandas.testing
import pytest

from PyPWA.plugins.data import sv, kv, numpy

ROOT = (Path(__file__).parent / "../../test_data/docs").resolve()
TEMP_LOCATION = ROOT / "temporary_write_data"

ALL = [
    {
        "parse": sv.metadata.get_memory_parser(),
        "reader": sv.metadata.get_reader,
        "writer": sv.metadata.get_writer,
        "can_read": sv.metadata.get_read_test(),
        "set1": [
            ROOT / "set1.csv",
            ROOT / "set1.tsv"
        ],
        "set2": [
            ROOT / "set2.csv",
            ROOT / "set2.tsv"
        ],
        "bad_set": [
            ROOT / "bad_set.csv"
        ],
        "wrong": [
            ROOT / "set1.kvars",
            ROOT / "set2.npy"
        ],
        "temp": [
            TEMP_LOCATION,
            Path(TEMP_LOCATION.stem + ".csv"),
            Path(TEMP_LOCATION.stem + ".tsv")
        ]
    },
    {
        "parse": kv.metadata.get_memory_parser(),
        "reader": kv.metadata.get_reader,
        "writer": kv.metadata.get_writer,
        "can_read": kv.metadata.get_read_test(),
        "set1": [ROOT / "set1.kvars"],
        "set2": [ROOT / "set2.kvars"],
        "bad_set": [ROOT / "bad_set.kvars"],
        "wrong": [
            ROOT / "set1.csv",
            ROOT / "set2.npy"
        ],
        "temp": [
            TEMP_LOCATION,
            Path(TEMP_LOCATION.stem + ".kvars")
        ]
    },
    {
        "parse": numpy.metadata.get_memory_parser(),
        "reader": numpy.metadata.get_reader,
        "writer": numpy.metadata.get_writer,
        "can_read": numpy.metadata.get_read_test(),
        "set1": [
            ROOT / "set1.txt",
            ROOT / "set1.pf",
            ROOT / "set1.npy"
        ],
        "set2": [
            ROOT / "set2.txt",
            ROOT / "set2.pf",
            ROOT / "set2.npy"
        ],
        "bad_set": [
            # We exclude bad_set.pf because numpy will parse it anyway
            ROOT / "bad_set.txt"
        ],
        "wrong": [
            ROOT / "set1.kvars",
            ROOT / "set2.csv"
        ],
        "temp": [
            Path(TEMP_LOCATION.stem + ".npy")
        ]
    }
]


# Test Array Length
@pytest.fixture(params=ALL, scope="module")
def get_plugin(request):
    return request.param


@pytest.fixture
def parser(get_plugin):
    return get_plugin['parse']


@pytest.fixture(params=[("set1", 1000), ("set2", 12)])
def data_set(get_plugin, request):
    return get_plugin[request.param[0]], request.param[1]


def test_array_length(parser, data_set):
    for data in data_set[0]:
        assert len(parser.parse(data)) == data_set[1]


# Test Bad Data
@pytest.fixture
def bad_set(get_plugin):
    return get_plugin["bad_set"]


def test_parse_bad_data_fails(parser, bad_set):
    for data in bad_set:
        with pytest.raises(Exception):
            parser.parse(data)


# Test can read correct data
@pytest.fixture
def can_read(get_plugin):
    return get_plugin["can_read"]


def test_can_read(data_set, can_read):
    for data in data_set[0]:
        assert can_read.can_read(data)


# Test can't read wrong data
@pytest.fixture
def wrong_data(get_plugin):
    return get_plugin["wrong"]


def test_cant_read_wrong_data(can_read, wrong_data):
    for data in wrong_data:
        assert not can_read.can_read(data)


# Test that data out equals data in
@pytest.fixture
def temp_location(get_plugin):
    return get_plugin["temp"]


@pytest.fixture(scope="module")
def pandas_flat():
    data = npy.zeros(30, [(name, "f8") for name in ['x', 'y', 'z']])
    for column in data.dtype.names:
        data[column] = npy.random.rand(30)
    return pandas.DataFrame(data)


def test_data_in_equals_data_out(parser, temp_location, pandas_flat):
    for location in temp_location:
        parser.write(location, pandas_flat)
        data = parser.parse(location)
        pandas.testing.assert_frame_equal(data, pandas_flat)
        location.unlink()


def test_reader_and_writer(get_plugin, pandas_flat):
    with get_plugin["writer"](get_plugin["temp"][0]) as writer:
        for index, value in pandas_flat.iterrows():
            writer.write(value)

    with get_plugin["reader"](get_plugin["temp"][0]) as reader:
        for value in reader:
            pass

    get_plugin["temp"][0].unlink()

"""
SV Specific Tests
"""


@pytest.fixture(params=["set1", "set2"])
def sv_data_sets(request):
    return ROOT / (request.param + ".csv"), ROOT / (request.param + ".tsv")


def test_tsv_matches_csv(sv_data_sets):
    pandas.testing.assert_frame_equal(
        sv.metadata.get_memory_parser().parse(sv_data_sets[0]),
        sv.metadata.get_memory_parser().parse(sv_data_sets[1])
    )


"""
Numpy Specific Tests
"""


def test_numpy_read_and_write_pf():
    pf_file = Path(TEMP_LOCATION.stem + ".pf")
    pass_fail = pandas.Series(npy.random.choice([True, False], 1000))

    numpy.metadata.get_memory_parser().write(pf_file, pass_fail)
    read = numpy.metadata.get_memory_parser().parse(pf_file)
    pf_file.unlink()

    pandas.testing.assert_series_equal(read, pass_fail)


def test_numpy_read_and_write_floats():
    float_file = Path(TEMP_LOCATION.stem + ".txt")
    floats = pandas.Series(npy.random.random(1000))

    numpy.metadata.get_memory_parser().write(float_file, floats)
    read = numpy.metadata.get_memory_parser().parse(float_file)
    float_file.unlink()

    pandas.testing.assert_series_equal(floats, read)


def test_numpy_reader_and_writer(pandas_flat):
    npy_file = Path(TEMP_LOCATION.stem + ".npy")
    data = pandas_flat[:100]

    with numpy.metadata.get_writer(npy_file) as writer:
        for index, event in data.iterrows():
            writer.write(event)

    with numpy.metadata.get_reader(npy_file) as reader:
        for index, event in enumerate(reader):
            pandas.testing.assert_series_equal(data.iloc[index], event)

    npy_file.unlink()
