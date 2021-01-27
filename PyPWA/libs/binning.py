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

from typing import Union, List, Optional as Opt

import numpy as npy
import pandas as pd


def bin_by_range(
        dataframe: Union[pd.DataFrame, npy.ndarray],
        bin_series: Union[npy.ndarray, pd.Series, str],
        number_of_bins: int, lower_cut: Opt[float] = None,
        upper_cut: Opt[float] = None, sample_size: Opt[int] = None
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
        same length as dataframe. If a column name is provided, that
        column will be used from the dataframe.
    number_of_bins : int
        The resulting number of bins that you would like to have.
    lower_cut : float, optional
        The lower cut off for the dataset, if not provided it will be set
        to the smallest value in the bin_series
    upper_cut : float, optional
        The upper cut off for the dataset, if not provided  will be set
        to the largest value in the bin_series
    sample_size : int, optional
        If provided each bin will have a randomly selected number of
        events of length sample_size.

    Returns
    -------
    List[DataFrame or Structured Array]
        A list of array-likes that have been masked off of the input
        bin_series.

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
    if isinstance(bin_series, str):
        bin_series = dataframe[bin_series]
    elif len(dataframe) != len(bin_series):
        raise ValueError("Input array and bin array must be the same length!")

    dataframe, bin_series = _mask_binned_data(
        dataframe, bin_series, lower_cut, upper_cut
    )

    bin_edges = npy.linspace(
        bin_series.min(), bin_series.max(), number_of_bins + 1
    )

    bin_masks = []
    for bin_count in range(len(bin_edges) - 1):
        bin_masks.append(
            _make_bin_values(
                bin_series, bin_edges[bin_count], bin_edges[bin_count + 1]
            )
        )

    bin_masks[-1] = _make_bin_values(
        bin_series, bin_edges[-2], bin_edges[-1], True
    )

    if sample_size:
        new_masks = []
        for mask in bin_masks:
            indexes = npy.arange(len(mask))[mask]
            choices = npy.random.choice(indexes, sample_size, False)
            new_mask = npy.zeros(len(mask), bool)
            new_mask[choices] = True
            new_masks.append(new_mask)
        bin_masks = new_masks

    bin_results = []
    for mask in bin_masks:
        binned_data = dataframe[mask]
        if sample_size:
            indexes = npy.arange(len(binned_data))
            sample_mask = npy.random.choice(indexes, sample_size, False)

            binned_data = binned_data[sample_mask.astype(bool)]
        bin_results.append(binned_data)

    return bin_results


def bin_with_fixed_widths(
        dataframe: Union[pd.DataFrame, npy.ndarray],
        bin_series: Union[npy.ndarray, pd.Series], fixed_size: int,
        lower_cut: Opt[float] = None, upper_cut: Opt[float] = None
) -> List[pd.DataFrame]:
    """Bins a dataframe by fixed using a series in memory

    Bins an input array by a fixed number of events in memory. You must
    put all data you  want binned into the DataFrame or Structured Array
    before use. Each resulting bin can be further binned if you desire.

    If the fixed_size does not evenly divide into the length of
    bin_series, the first and last bin will contain overflows.

    Parameters
    ----------
    dataframe : DataFrame or Structured Array
        The dataframe or numpy array that you wish to break into bins
    bin_series : Array-like
        Data that you want to bin by, selectable by user. Must have the
        same length as dataframe. If a column name is provided, that
        column will be used from the dataframe.
    fixed_size : int
        The number of events you want in each bin.
    lower_cut : float, optional
        The lower cut off for the dataset, if not provided it will be set
        to the smallest value in the bin_series
    upper_cut : float, optional
        The upper cut off for the dataset, if not provided  will be set
        to the largest value in the bin_series
    Returns
    -------
    List[DataFrame or Structured Array]
        A list of array-likes that have been masked off of the input
        bin_series.

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
    >>> range_bins = bin_with_fixed_widths(df, binning, 250)
    >>> len(range_bins)
    4

    Each bin should have exactly 250 events in size

    >>> lengths = []
    >>> for abin in range_bins:
    >>>    lengths.append(len(abin))
    [250, 250, 250, 250]

    That will give you 4 bins with exaactly the same number of events
    per bin, plus 2 more bins if needed.
    """
    if isinstance(bin_series, str):
        bin_series = dataframe[bin_series]
    elif len(dataframe) != len(bin_series):
        raise ValueError("Input array and bin array must be the same length!")

    dataframe, bin_series = _mask_binned_data(
        dataframe, bin_series, lower_cut, upper_cut
    )

    indexes = bin_series.argsort().argsort().astype("u4")

    num_in_center = len(indexes) // fixed_size
    lower_events = (len(indexes) % fixed_size) // 2
    upper_events = lower_events + (num_in_center * fixed_size)

    bins = []
    if lower_events:
        lower_slice = _make_bin_values(indexes, 0, lower_events)
        bins.append(dataframe[lower_slice])

    for i in range(num_in_center):
        lower_value = lower_events + (i * fixed_size)
        upper_value = lower_events + (fixed_size * (i + 1))
        mask = _make_bin_values(indexes, lower_value, upper_value)
        bins.append(dataframe[mask])

    if upper_events != len(bin_series):
        upper_slice = _make_bin_values(
            indexes, upper_events, len(indexes), True
        )
        bins.append(dataframe[upper_slice])

    return bins

def bin_by_list(
    data: Union[pd.DataFrame, npy.ndarray],
    bin_series: Union[npy.ndarray, pd.Series, str],
    bin_list : List
) -> List[pd.DataFrame]:
    """Bins a dataframe by list of bin limits using a series in memory

    Bins an input array by list of bin limits in memory. You must put all data
    you want binned into the DataFrame or Structured Array before use. Each
    resulting bin can be further binned if you desire.

    Parameters
    ----------
    dataframe : DataFrame or Structured Array
        The dataframe or numpy array that you wish to break into bins
    bin_series : Array-like
        Data that you want to bin by, selectable by user. Must have the
        same length as dataframe. If a column name is provided, that
        column will be used from the dataframe.
    bin_list : list
        The list of bin limits used to create the bins.

    Returns
    -------
    List[DataFrame or Structured Array]
        A list of array-likes that have been masked off of the input
        bin_series.

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


    Examples
    --------
    Binning a DataFrame with values x, y, and z using z to bin

    First create the list which defines all the bin limits
    >>> bin_limits = [1,3,7,10]

    >>> data = {
    >>>     "x": npy.random.rand(1000), "y": npy.random.rand(1000),
    >>>     "z": (npy.random.rand(1000) * 100) - 50
    >>>    }
    >>> df = pd.DataFrame(data)
    >>> list(df.columns)
    ["x", "y", "z"]

    This will give us a usable DataFrame, now to make a series out of z
    and use it to make the 3 defined bins bins.

    >>> binning = df["z"]
    >>> range_bins = bin_by_list(df, binning, bin_limits)
    >>> len(range_bins)
    3

    That will give you 3 bins with custom bin limits
    """
    binneddata = []
    for i in range(len(bin_list)-1):
        tempbin = bin_by_range(data, bin_series, 1, bin_list[i], bin_list[i+1])
        binneddata.append(tempbin[0])
    return binneddata


def _mask_binned_data(
        array: Union[npy.ndarray, pd.DataFrame],
        bin_values: Union[pd.Series, npy.ndarray],
        lower: Opt[float] = None, upper: Opt[float] = None
):
    if lower is None:
        lower = bin_values.min()
    if upper is None:
        upper = bin_values.max()
    kept = _make_bin_values(bin_values, lower, upper, True)
    return array[kept], bin_values[kept]


def _make_bin_values(
        array: Union[npy.ndarray, pd.Series], lower: float, upper: float,
        last: Opt[bool] = False
):
    if last:
        upper_series = array <= upper
    else:
        upper_series = array < upper
    lower_series = array >= lower
    return npy.logical_and(lower_series, upper_series)
