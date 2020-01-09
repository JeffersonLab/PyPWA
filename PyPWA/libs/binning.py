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

from typing import Union, List

import numpy as npy
import pandas as pd


def bin_by_range(
        dataframe: pd.DataFrame,
        bin_series: Union[npy.ndarray, pd.Series], number_of_bins: int
) -> List[pd.DataFrame]:
    """Bins a dataframe by range using a series in memory

    Bins an input array by range in memory. You must put all data you want
    binned into the DataFrame or Structured Array before use. Each
    resulting bin can be further binned if you desire.

    Parameters
    ----------
    dataframe : DataFrame or Structured Array
        The dataframe or numpy array that you wish to break into bins
    bin_series : Array-like
        Data that you want to bin by, selectable by user. Must have the
        same length as dataframe
    number_of_bins : int
        The resulting number of bins that you would like to have.

    Returns
    -------
    List[DataFrame or Structured Array]
        A list of array-likes that have been masked off of the input
        dataframe.

    Raises
    ------
    ValueError
        If the length of the input array and bin array don't match

    Warnings
    --------
    This function does all binning in memory, if you are working with
    a large dataset that doesn't fit in memory, or if you overflow while
    you are binning, you must use a different binning method

    See Also
    --------
    PyPWA.libs.file.project : A numerical dataset that supports binning
        on disk instead of in-memory. It's slower and requires more steps
        to use, but should work even on memory limited systems.

    Notes
    -----
    The range is selected using a simple method:

    .. math:: (max - min) / num_of_bins


    Examples
    --------
    Binning a DataFrame with values x, y, and z using z to bin

    >>> data = {
    >>>     "x": npy.random.rand(1000), "y": npy.random.rand(1000),
    >>>     "z": (npy.random.rand(1000) * 100) - 50
    >>>    }
    >>> df = pd.DataFrame(data)
    >>> list(df.columns)
    ["x", "y", "z"]

    This will give us a usable DataFrame, now to make a series out of z
    and use it to make 10 bins.

    >>> binning = df["z"]
    >>> range_bins = bin_by_range(df, binning, 10)
    >>> len(range_bins)
    10

    That will give you 10 bins with a very close number of values per bin
    """
    if len(dataframe) != len(bin_series):
        raise ValueError("Input array and bin array must be the same length!")

    bin_edges = npy.linspace(
        bin_series.min(), bin_series.max(), number_of_bins
    )

    bin_results = []
    for bin_count in range(len(bin_edges) - 1):
        bin_mask = _make_bin_values(
            bin_series, bin_edges[bin_count], bin_edges[bin_count + 1]
        )

        bin_results.append(dataframe[bin_mask])

    return bin_results


def _make_bin_values(array: npy.ndarray, lower: float, upper: float):
    lower_series = array > lower
    upper_series = array < upper
    return npy.logical_and(lower_series, upper_series)
