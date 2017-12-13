# coding=utf-8

import os

import pytest

from PyPWA.builtin_plugins import nestle
from PyPWA.libs import configuration_db


SIMPLE_PRIOR = os.path.join(
    os.path.dirname(__file__), "../../test_data/source_files/simple_prior.py"
)


@pytest.fixture()
def nested():
    db = configuration_db.Connector()
    db.initialize_component("nestle", nestle.NestleOptions().get_defaults())
    db.merge_component(
        "nestle",
        {
            "prior location": SIMPLE_PRIOR,
            "prior name": "prior",
            "method": "classic",
            "npoints": 4,
            "parameters": ["A"]
        }
    )

    return nestle.NestleOptions().get_optimizer()


@pytest.fixture()
def nested_save_data(nested):
    yield nested
    nested.save_extra("extra_data")
    os.remove("extra_data.npy")
    os.remove("extra_data.txt")


def test_nested_with_save(nested_save_data):
    logl = lambda x: 0.0
    nested_save_data.run(logl)
