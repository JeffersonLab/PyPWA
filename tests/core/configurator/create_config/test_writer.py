import os

import pytest

from PyPWA.core.configurator.create_config import _writer


CONFIGURATION = {
    "Shell Options":
        {
            "Option1": "string",
            "Option2": False,
            "Option3": 123,
            "Option4": [1,2,3]
        }
}


@pytest.fixture()
def writer():
    return _writer.Write()


def test_yml_writer(writer):
    writer.write(CONFIGURATION, "test_config.yml")
    os.remove("test_config.yml")


def test_json_writer(writer):
    writer.write(CONFIGURATION, "test_config.json")
    os.remove("test_config.json")
