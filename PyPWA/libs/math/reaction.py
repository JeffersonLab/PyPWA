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

"""

"""

import numpy as npy
from PyPWA.libs.math import vectors


_PROTON_GEV = .9382720813


def get_event_mass(collection: vectors.ParticlePool) -> npy.ndarray:
    found_photon, found_proton = 0, 0
    vector_sum = vectors.FourVector(collection.event_count)
    for event_particle in collection.iter_particles():
        if not found_photon and event_particle.id == 1:
            found_photon = True
        elif not found_proton and event_particle.id == 14:
            found_proton = True
        else:
            vector_sum += event_particle
    return vector_sum.get_mass()


def get_t(collection: vectors.ParticlePool) -> npy.ndarray:
    proton = collection.get_particles_by_name("Proton")[0]
    momenta = proton.x**2 + proton.y**2 + proton.z**2
    energy = (proton.e - _PROTON_GEV)**2
    return energy - momenta


def get_s(collection: vectors.ParticlePool) -> npy.ndarray:
    proton = collection.get_particles_by_name("Proton")[0]
    momenta = proton.x**2 + proton.y**2 + proton.z**2
    energy = (proton.e + _PROTON_GEV)**2
    return energy - momenta


def get_t_prime(collection: vectors.ParticlePool) -> npy.ndarray:
    # Get initial values
    proton = collection.get_particles_by_name("Proton")[0]
    s_value = get_s(collection)
    sqrt_s = npy.sqrt(s_value)
    mx2 = get_event_mass(collection)**2

    # Calculate for Px and Ex
    ex = (s_value * mx2 * _PROTON_GEV**2) / 2 * sqrt_s
    px = npy.sqrt((ex**2) - mx2)

    # Calculate t0
    t0_left = (mx2 / (2 * sqrt_s))**2
    t0_right = (((proton.e * _PROTON_GEV) / sqrt_s) - px)**2
    t0 = t0_left - t0_right

    return get_t(collection) - t0
