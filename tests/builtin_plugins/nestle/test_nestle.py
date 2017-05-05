import os

import pytest

from PyPWA.builtin_plugins import nestle
from PyPWA.core.configurator import option_tools

SIMPLE_PRIOR = os.path.join(
    os.path.dirname(__file__), "../../data/source_files/simple_prior.py"
)


def simple_function(x):
    return 0.0


@pytest.fixture()
def nested():
    template = nestle.NestleOptions.default_options
    options = {
        "prior location": SIMPLE_PRIOR,
        "prior name": "prior",
        "method": "classic",
        "npoints": 4
    }
    command = option_tools.CommandOptions(template, options)
    setup = nestle.NestleOptions.setup(command)
    return setup.return_interface()


@pytest.fixture()
def nested_save_data(nested):
    yield nested
    nested.save_extra("extra_data")
    os.remove("extra_data.npy")
    os.remove("extra_data.txt")


def test_nested_with_save(nested_save_data):
    logl = lambda x: 0.0
    nested_save_data.main_options(logl)
    nested_save_data.start()
