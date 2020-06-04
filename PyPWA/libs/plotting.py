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


from typing import Union, Optional as Opt

import matplotlib.pyplot as plt
import numpy as npy
import pandas as pd
from matplotlib import cm
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D


def make_lego(
        x_data: Union[npy.ndarray, pd.Series],
        y_data: Union[npy.ndarray, pd.Series],
        bins: Opt[int] = None,
        cmap: Opt[Union[str, colors.ListedColormap]] = "jet",
        ax: Opt[Axes3D] = None, elev: Opt[int] = 10, azim: Opt[int] = 215
):
    """
    Produces a 3D Lego plot, similar to what is produced by ROOT. This is
    similar to a 2D Histogram, but treats x and y as x and z, and projects
    the occurrences into the y dimension.

    Parameters
    ----------
    x_data : ndarray or Series
        X data for the lego plot
    y_data : ndarray or Series
        Y data for the lego plot
    bins : int, optional
        Number of bins to create when making the lego plot.
    cmap : str or matplotlib.colors.ListedColormap, optional
        cmap to use when creating the lego plot. It takes either a string
        of the name for matplotlib, or a matplotlib cmap
    ax : Axes3D, optional
        An axes object to place the lego plot into. The axes must be an
        axes that supports 3d projection or it will cause the function
        to error.
    elev : int, optional
        Adjusts the elevation of the lego-plot
    azim : int, optional
        Adjusts the azimuth of the resulting image. It's value is a angle
        between 0 and 360 degrees.

    Returns
    -------
    Axes3D
        The axes object of the plot

    Notes
    -----
    If the number of bins isn't provided, it's instead calculated using
    one half of Sturge's Rule rounded up:

    .. math::
        ceil(\frac{1 + 3.322 \cdot log(N_{events})}{2})
    """

    if bins is None:
        bins = npy.ceil((1 + 3.322 * npy.log(len(x_data))) / 2)

    if ax is None:
        fig = plt.figure()
        ax = Axes3D(fig)

    hist, xedges, yedges = npy.histogram2d(x_data, y_data, bins=(bins, bins))
    xpos, ypos = npy.meshgrid(
        xedges[:-1] + xedges[1:], yedges[:-1] + yedges[1:]
    )

    xpos = xpos.flatten() / 2
    ypos = ypos.flatten() / 2
    zpos = npy.zeros_like(xpos)

    dx = xedges[1] - xedges[0]
    dy = yedges[1] - yedges[0]
    dz = hist.flatten()

    if isinstance(cmap, str):
        cmap = cm.get_cmap(cmap)
    elif not isinstance(cmap, colors.ListedColormap):
        raise ValueError("cmap not understood!")

    max_height = npy.max(dz)
    min_height = npy.min(dz)
    rgba = [cmap((k - min_height) / max_height) for k in dz]

    ax.view_init(elev, azim)
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, alpha=1, color=rgba, zsort="average")
    return ax
