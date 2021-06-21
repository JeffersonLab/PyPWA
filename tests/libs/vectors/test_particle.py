import numpy as np

from PyPWA.libs import vectors


def test_particle_pool_can_get_by_id(random_particle_pool):
    fetched_particle = random_particle_pool.get_particles_by_id(1)
    assert fetched_particle[0].id == 1


def test_particle_pool_can_get_by_name(random_particle_pool):
    fetched_particle = random_particle_pool.get_particles_by_name("Gamma")
    assert fetched_particle[0].name == "Gamma"


def test_particle_pool_length(random_particle_pool):
    assert random_particle_pool.particle_count == 5


def test_particle_pool_event_count(random_particle_pool):
    assert random_particle_pool.event_count == 500


def test_particle_pool_event_iterator(random_particle_pool):
    assert len(list(random_particle_pool.iter_events())) == 500


def test_particle_pool_particle_iterator(random_particle_pool):
    assert len(list(random_particle_pool.iter_particles())) == 5


def test_particle_pool_iterates_over_events(random_particle_pool):
    for index, particle_event in enumerate(random_particle_pool.iter_events()):
        assert isinstance(particle_event, vectors.ParticlePool)
    assert index == 499


def test_particle_pool_split(random_particle_pool):
    split = random_particle_pool.split(4)
    for chunk in split:
        particle_length = 0
        for index, particle in enumerate(chunk.iter_particles()):
            if index == 0:
                particle_length = len(particle)
            assert len(particle) == particle_length


def test_particle_can_do_math():
    a = vectors.Particle(1, 1, 1.0, 2.0, 3.0, 4.0)
    b = vectors.Particle(14, 1, 1.1, 2.1, 3.1, 4.1)
    c = (a + b) * 2

    assert c.e == 4.2
    assert c.x == 8.2
    assert c.y == 12.2
    assert c.z == 16.2


def test_particle_raw_display(random_particle_pool):
    random_particle_pool.display_raw()


def test_particle_pool_can_be_masked(random_particle_pool):
    mask = np.random.choice([True, False], random_particle_pool.event_count)
    result = random_particle_pool[mask]
    assert result.event_count == sum(mask)
