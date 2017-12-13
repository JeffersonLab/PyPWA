import numpy
import pytest

from PyPWA.progs.shell import loaders
from PyPWA.progs.shell.fit.likelihoods import empty
from PyPWA.libs.components.optimizers import opt_plugins


class Data(loaders.DataLoading):

    __DATA = numpy.random.rand(4500)

    def __init__(self):
        pass

    @property
    def data(self):
        return self.__DATA


class Functions(loaders.FunctionLoader):

    def __init__(self):
        pass

    def setup(self):
        pass

    def process(self, data, data2):
        return data + data2


@pytest.fixture()
def likelihood_loader():
    loader = empty.EmptyLikelihood()
    loader.setup_likelihood(
        Data(), Functions(), opt_plugins.Type.MAXIMIZER
    )
    return loader


@pytest.fixture()
def data(likelihood_loader):
    return likelihood_loader.get_data()['data']


@pytest.fixture()
def likelihood(likelihood_loader, data):
    likelihood = likelihood_loader.get_likelihood()
    likelihood.data = data
    return likelihood


def test_empty_likelihood(likelihood, data):
    computed = data + 1
    returned = likelihood.process(1)
    assert computed.sum() == returned.sum()
