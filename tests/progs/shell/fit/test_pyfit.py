import pytest

from PyPWA.progs.shell.fit import pyfit


@pytest.fixture()
def likelihood_finder():
    return pyfit.LikelihoodPackager()


def test_finder_finds_chi_squared(likelihood_finder):
    assert "chi-squred" in likelihood_finder.get_likelihood_name_list()


def test_finder_finds_chi_squared(likelihood_finder):
    assert "likelihood" in likelihood_finder.get_likelihood_name_list()


def test_finder_finds_chi_squared(likelihood_finder):
    assert "empty" in likelihood_finder.get_likelihood_name_list()

