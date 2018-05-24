from PyPWA.libs.math import particle


def test_particle_pool_can_get_by_id(random_particle_pool):
    fetched_particle = random_particle_pool.get_particles_by_id(1)
    assert fetched_particle[0].id == 1


def test_particle_pool_can_get_by_name(random_particle_pool):
    fetched_particle = random_particle_pool.get_particles_by_name("Gamma")
    assert fetched_particle[0].name == "Gamma"


def test_particle_pool_length(random_particle_pool):
    assert len(random_particle_pool) == 5
    assert random_particle_pool.particle_count == 5


def test_particle_pool_event_count(random_particle_pool):
    assert random_particle_pool.event_count == 500


def test_particle_pool_event_iterator(random_particle_pool):
    assert len(list(random_particle_pool.iterate_over_events())) == 500


def test_particle_pool_particle_iterator(random_particle_pool):
    assert len(list(random_particle_pool.iterate_over_particles())) == 5


def test_particle_pool_iterates_over_events(random_particle_pool):
    for index, particle_event in enumerate(random_particle_pool):
        assert isinstance(particle_event, particle.ParticlePool)
    assert index == 499


def test_particle_pool_split(random_particle_pool):
    split = random_particle_pool.split(4)
    for chunk in split:
        particle_length = 0
        for index, particle in enumerate(chunk.iterate_over_particles()):
            if index == 0:
                particle_length = len(particle)
            assert len(particle) == particle_length
