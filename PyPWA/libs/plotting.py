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


import matplotlib.pyplot as _plt
import numpy as _npy

from matplotlib import cm as _cm
from mpl_toolkits.mplot3d import Axes3D as _Axes3D


def make_lego(x_data, y_data, bins, cmap="jet"):
    """
    Produces a 3D Lego plot, similar to what is produced by ROOT. This is
    similar to a 2D Histogram, but treats x and y as x and z, and projects
    the occurrences into the y dimension.

    Parameters
    ----------
    x_data : ndarray or Series
    y_data : ndarray or Series
    bins : int

    Returns
    -------
    Axes3D

    """
    fig = _plt.figure()
    ax = _Axes3D(fig)

    hist, xedges, yedges = _npy.histogram2d(x_data, y_data, bins=(bins, bins))
    xpos, ypos = _npy.meshgrid(
        xedges[:-1] + xedges[1:], yedges[:-1] + yedges[1:]
    )

    xpos = xpos.flatten() / 2
    ypos = ypos.flatten() / 2
    zpos = _npy.zeros_like(xpos)

    dx = xedges[1] - xedges[0]
    dy = yedges[1] - yedges[0]
    dz = hist.flatten()

    cmap = _cm.get_cmap(cmap)
    max_height = _npy.max(dz)
    min_height = _npy.min(dz)
    rgba = [cmap((k - min_height) / max_height) for k in dz]

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, alpha=1, color=rgba, zsort="average")
    return ax
