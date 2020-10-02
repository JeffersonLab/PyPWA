import numpy as np
import pandas as pd

import pytest


@pytest.fixture
def structured_data():
    data = np.empty(1000, [("a", "f8"), ("b", "f8")])
    data["a"] = np.random.rand(1000)
    data["b"] = np.random.rand(1000)
    return data


"""
Since all the plugins _should_ use the same interface, the actual tests
for them have been generalized here. If you feel that a test needs to be
altered to fit a specific plugin, then you're probably not following the
interface closely, and will more than likely break compatibility with
the Data Module.
"""


@pytest.fixture
def check_iterator_passes_data():
    """
    This is the only test here that is _optional_ for iterators. An
    iterator is not required to pass a pointer, though it is strongly
    encouraged for speed reasons. If you have a file type that only
    supports parsing the entire file, and then you have to fake iterating
    over it, then this can be ignored.

    .. seealso::
        The numpy plugin, since it has to fake iteration and can not
        pass a single pointer.
    """
    def iterator_check(initialized_iterator):
        first_result = next(initialized_iterator)
        second_result = next(initialized_iterator)
        return first_result == second_result
    return iterator_check


@pytest.fixture
def check_memory_read_write():
    def check_memory(parser, data, location):
        # Write and parse data
        parser.write(location, data)
        parsed_data = parser.parse(location)

        # Remove temporary file
        location.unlink()

        # Check data matches
        for name in data.dtype.names:
            np.testing.assert_array_almost_equal(
                data[name], parsed_data[name]
            )
    return check_memory


@pytest.fixture
def iterate_numpy_arrays():
    def numpy_array(iterator, data, location):
        # Write data with iterator
        with iterator["writer"](location) as writer:
            for row in data:
                writer.write(row)

        # Read data from file
        read_rows = []
        with iterator["reader"](location, False) as reader:
            for event in reader:
                read_rows.append(event.copy())
        read_data = np.array(read_rows)

        # Compare read data with structured data
        for name in read_data.dtype.names:
            np.testing.assert_array_almost_equal(
                data[name],
                read_data[name]
            )

        # Remove temporary file
        location.unlink()
    return numpy_array


@pytest.fixture
def iterate_dataframe():
    def dataframe_check(iterator, data, location):
        dataframe = pd.DataFrame(data)

        # Write data with iterator
        with iterator["writer"](location) as writer:
            for index, row in dataframe.iterrows():
                writer.write(row)

        # Read data from file
        read_data = []
        with iterator["reader"](location, True) as reader:
            for row in reader:
                read_data.append(row)
        read_data = pd.DataFrame(read_data)

        pd.testing.assert_frame_equal(dataframe, read_data)

        # Remove temporary file
        location.unlink()
    return dataframe_check

