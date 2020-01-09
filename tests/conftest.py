# coding=utf-8

import numpy
import pytest

from PyPWA.libs import vectors


def make_new_particle(geant_id):
    p = vectors.Particle(geant_id, 500)
    p.x, p.y = numpy.random.rand(500), numpy.random.rand(500)
    p.z, p.e = numpy.random.rand(500), numpy.random.rand(500)
    return p


def make_new_particle_pool():
    new_particle_pool = []
    for geant_id in [1, 3, 4, 7, 13]:
        new_particle_pool.append(make_new_particle(geant_id))
    return vectors.ParticlePool(new_particle_pool)


@pytest.fixture(scope="module")
def random_particle_pool():
    return make_new_particle_pool()
