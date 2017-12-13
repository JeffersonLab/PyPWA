import numpy
import pytest

from PyPWA.progs.shell import loaders
from PyPWA.progs.shell.fit.likelihoods import chi_squared
from PyPWA.libs.components.optimizers import opt_plugins


class Functions(loaders.FunctionLoader):

    def __init__(self):
        pass

    def setup(self):
        pass

    def process(self, data, data2):
        return data + data2


class BaseData(loaders.DataLoading):

    __DATA = numpy.random.rand(4500)

    def __init__(self):
        pass

    @property
    def data(self):
        return self.__DATA

    @property
    def qfactor(self):
        return numpy.ones(4500)

    @property
    def binned(self):
        return numpy.ones(4500)

    @property
    def expected_values(self):
        return numpy.ones(4500)

    @property
    def event_errors(self):
        return numpy.ones(4500)


@pytest.fixture()
def data():
    return BaseData().data


"""
Test Binned Chi-Squared
"""

class BinnedData(BaseData):

    __BINNED = numpy.random.rand(4500)


    def __init__(self):
        pass

    @property
    def binned(self):
        return self.__BINNED


@pytest.fixture()
def binned():
    return BinnedData().binned


@pytest.fixture()
def binned_loader():
    likelihood_loader = chi_squared.ChiLikelihood()
    likelihood_loader.setup_likelihood(
        BinnedData(), Functions(), opt_plugins.Type.MINIMIZER
    )
    return likelihood_loader


def test_binned_data_matches(binned_loader, data, binned):
    assert binned_loader.get_data()['data'].sum() == data.sum()
    assert binned_loader.get_data()['binned'].sum() == binned.sum()


@pytest.fixture()
def binned_chi_value(binned_loader, data, binned):
    likelihood = binned_loader.get_likelihood()
    likelihood.data = data
    likelihood.binned = binned
    return likelihood.process(1)


def test_binned_value_matches_expected(binned_chi_value, data, binned):
    value = numpy.sum(((data + 1) - binned)**2 / binned)
    assert binned_chi_value == value


"""
Test UnBinned Chi-Squared
"""

class UnBinnedData(BaseData):

    __EXPECTED = numpy.random.rand(4500)
    __ERRORS = numpy.random.rand(4500)

    @property
    def expected_values(self):
        return self.__EXPECTED

    @property
    def event_errors(self):
        return self.__ERRORS


@pytest.fixture()
def expected():
    return UnBinnedData().expected_values

@pytest.fixture()
def errors():
    return UnBinnedData().event_errors


@pytest.fixture()
def un_binned_loader():
    likelihood_loader = chi_squared.ChiLikelihood()
    likelihood_loader.setup_likelihood(
        UnBinnedData(), Functions(), opt_plugins.Type.MAXIMIZER
    )
    return likelihood_loader


def test_un_binned_data_matches(un_binned_loader, data, expected, errors):
    values = un_binned_loader.get_data()
    assert values['data'].sum() == data.sum()
    assert values['event errors'].sum() == errors.sum()
    assert values['expected values'].sum() == expected.sum()


@pytest.fixture()
def un_binned_chi_value(un_binned_loader, data, expected, errors):
    likelihood = un_binned_loader.get_likelihood()
    print(type(data), type(expected), type(errors))
    likelihood.data = data
    likelihood.expected = expected
    likelihood.error = errors
    return likelihood.process(1)


def test_un_binned_value_matches_expected(
        un_binned_chi_value, data, expected, errors
):
    value = -1. * numpy.sum(((data + 1) - expected)**2 / errors)
    assert value == un_binned_chi_value


"""
Test No Likelihood Found
"""

def test_no_binned_or_errors():
    likelihood_loader = chi_squared.ChiLikelihood()
    with pytest.raises(ValueError):
        likelihood_loader.setup_likelihood(
            BaseData(), Functions(), opt_plugins.Type.MAXIMIZER
        )
