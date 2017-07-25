import numpy
import pytest

from PyPWA.progs.shell import loaders
from PyPWA.progs.shell.fit.likelihoods import log_likelihood
from PyPWA.libs.interfaces import optimizers


class Functions(loaders.FunctionLoader):

    def __init__(self):
        pass

    def setup(self):
        pass

    def process(self, data, data2):
        return data + data2


class BaseData(loaders.DataLoading):

    __DATA = numpy.random.rand(4500)
    __QFACTOR = numpy.random.rand(4500)
    __BINNED = numpy.random.rand(4500)

    def __init__(self):
        pass

    @property
    def data(self):
        return self.__DATA

    @property
    def qfactor(self):
        return self.__QFACTOR

    @property
    def monte_carlo(self):
        return None

    @property
    def binned(self):
        return self.__BINNED

    @property
    def expected_values(self):
        return numpy.ones(4500)

    @property
    def event_errors(self):
        return numpy.ones(4500)


@pytest.fixture()
def data():
    return BaseData().data


@pytest.fixture()
def qfactor():
    return BaseData().qfactor


@pytest.fixture()
def binned():
    return BaseData().binned


"""
Test UnExtended Likelihood
"""


@pytest.fixture()
def un_extended_loader():
    likelihood_loader = log_likelihood.LogLikelihood()
    likelihood_loader.setup_likelihood(
        BaseData(), Functions(), optimizers.OptimizerTypes.MINIMIZER
    )
    return likelihood_loader


def test_un_extended_data_matches(un_extended_loader, data, qfactor, binned):
    values = un_extended_loader.get_data()
    assert values['data'].sum() == data.sum()
    assert values['qfactor'].sum() == qfactor.sum()
    assert values['binned'].sum() == binned.sum()


@pytest.fixture()
def un_extended_value(un_extended_loader, data, qfactor, binned):
    likelihood = un_extended_loader.get_likelihood()
    likelihood.data = data
    likelihood.qfactor = qfactor
    likelihood.binned = binned
    return likelihood.process(1)


def test_un_expected_value_matches_expected(
        un_extended_value, data, qfactor, binned
):
    value = -1. * qfactor * binned * numpy.log(data+1)
    assert un_extended_value.sum() == value.sum()


"""
Test Extended Likelihood
"""


class ExtendedData(BaseData):

    __MONTE_CARLO = numpy.random.rand(4500)

    def __init__(self):
        pass

    @property
    def monte_carlo(self):
        return self.__MONTE_CARLO


@pytest.fixture()
def monte_carlo():
    return ExtendedData().monte_carlo


@pytest.fixture()
def extended_loader():
    likelihood_loader = log_likelihood.LogLikelihood()
    likelihood_loader.setup_likelihood(
        ExtendedData(), Functions(), optimizers.OptimizerTypes.MAXIMIZER,
        {"generated length": 1000000}
    )
    return likelihood_loader


@pytest.fixture()
def test_extended_data_matches(extended_loader, monte_carlo):
    value = extended_loader.get_data()
    assert value['monte carlo'].sum() == monte_carlo.sum()


@pytest.fixture()
def extended_value(extended_loader, data, monte_carlo, qfactor):
    likelihood = extended_loader.get_likelihood()
    likelihood.data = data
    likelihood.monte_carlo = monte_carlo
    likelihood.qfactor = qfactor
    return likelihood.process(1)


def test_extended_matches_expected(
        extended_value, data, monte_carlo, qfactor
):
    data = numpy.sum(qfactor * numpy.log(data + 1))
    mc = 1/1000000. * numpy.sum(monte_carlo + 1)
    expected = data + mc
    assert expected == extended_value.sum()
