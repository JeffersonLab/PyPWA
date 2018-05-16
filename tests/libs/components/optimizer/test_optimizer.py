# coding=utf-8

import pytest


from PyPWA.libs.components.optimizers import gateway
from PyPWA.libs import configuration_db


@pytest.fixture
def minuit():
    configuration_db.Connector().initialize_component(
        "Optimizer",
        {
            "parameters": ["A1"],
            "selected optimizer": "minuit",
            "configuration": {
                "settings": {
                    "A1": 1,
                    "errordef": 1,
                    "error_A1": 1
                },
                "strategy": 0,
                "number of calls": 1,
            }
        }
    )


@pytest.fixture(scope="function")
def minuit_optimizer(minuit):
    optimizer = gateway.FetchOptimizer()
    return optimizer


def test_prior(minuit_optimizer):
    logl = lambda x: 0.0
    minuit_optimizer.run(logl)
