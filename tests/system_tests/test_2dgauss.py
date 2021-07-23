import numpy as npy
import pandas as pd

import PyPWA as pwa
import numexpr as ne
import pytest


class Gauss2dAmplitude(pwa.NestedFunction):

    def setup(self, array, initial_params=""):
        self.__data = array

    def calculate(self, params):
        valueA = (self.__data["x"] - params["A1"]) ** 2
        valueA /= params["A2"] ** 2
        valueB = (self.__data["y"] - params["A3"]) ** 2
        valueB /= params["A4"] ** 2

        values = 1 / (params["A2"] * params["A4"])
        values *= npy.exp(-(valueA + valueB))
        return values


class NeGauss2dAmplitude(pwa.NestedFunction):

    USE_MP = False

    def setup(self, array, initial_params=""):
        self.__data = array

    def calculate(self, params):
        return ne.evaluate(
            "(1/(a2*a4)) * exp(-((((x-a1)**2)/(a2**2))+(((y-a3)**2)/(a4**2))))",
            local_dict={
                "a1": params["A1"], "a2": params["A2"], "a3": params["A3"],
                "a4": params["A4"], "x": self.__data["x"], "y": self.__data["y"]
            }
        )


@pytest.fixture(params=[Gauss2dAmplitude, NeGauss2dAmplitude])
def gauss_function(request):
    return request.param


def test_2d_gauss(gauss_function):
    flat_data = pd.DataFrame()
    flat_data["x"] = npy.random.rand(10000) * 20
    flat_data["y"] = npy.random.rand(10000) * 20

    simulation_params = {"A1": 10, "A2": 3, "A3": 10, "A4": 3}
    rejection = pwa.monte_carlo_simulation(
        gauss_function(), flat_data, simulation_params
    )

    carved_data = flat_data[rejection]

    fitting_settings = {
        "errordef": 1, "pedantic": False,
        "A1": 1, "limit_A1": [.1, None],
        "A2": 1, "limit_A2": [1, None],
        "A3": 1, "limit_A3": [.1, None],
        "A4": 1, "limit_A4": [1, None],
    }

    param_names = ["A1", "A2", "A3", "A4"]

    with pwa.LogLikelihood(gauss_function(), carved_data) as likelihood:
        results = pwa.minuit(param_names, fitting_settings, likelihood, 1)

    for param in results.params:
        assert simulation_params[param.name] == round(param.value)


