import pytest

from PyPWA import Path
from PyPWA.initializers.configurator.create_config import _writer

ROOT = Path()
YAML_DATA = ROOT / "test_config.yml"
JSON_DATA = ROOT / "test_config.json"


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
    writer.write(CONFIGURATION, YAML_DATA)
    YAML_DATA.unlink()


def test_json_writer(writer):
    writer.write(CONFIGURATION, JSON_DATA)
    JSON_DATA.unlink()
