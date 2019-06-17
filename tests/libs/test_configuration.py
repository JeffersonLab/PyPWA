#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016 JLab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pathlib import Path
from typing import Any, Dict

import pytest

from PyPWA.libs import configuration

# Set NO_FUZ so that we can skip tests that will fail without fuzzywuzzy
try:
    import fuzzywuzzy.process
    NO_FUZ = False
except ImportError:
    NO_FUZ = True

"""
Layout
------
- Example Configurations and Template: Includes globals
- Fixtures and helping functions
- Tests
    - Data with bad spelling
    - Writing and reading basic configuration files without spelling errors
    - Bad data
"""

"""
Example Configurations and Template
"""

TEMPLATE = {
    "Name": str,
    "Do Read": bool,
    "Count": int,
    "Percentage": float,
    "Extended": {
        "Parameters": list,
        "Sets": set,
        "Level": ["Debug", "Info", "Error"]
    }
}

CONFIGURATION1 = {
    "Name": "Example",
    "Do Read": True,
    "Count": 42,
    "Percentage": .754,
    "Extended": {
        "Parameters": ["A1", "A2", "A3"],
        "Level": "Debug"
    },
    "Extra": None
}

CONFIGURATION2 = {
    "Name": "Example",
    "Do Read": True,
    "Count": 42,
    "Percentage": None,
    "Extended": {
        "Parameters": ["A1"],
        "Sets": {"A1", "A2"},
        "Level": "Debug"
    }
}

# Errors without fuzzywuzzy
LIGHT_ERROR = {
    "Name": 5,
    "Do Read": "1",
    "Count": 42.0,
    "Percentage": None,
    "Extended": {
        "Parameters": "A1",
        "Sets": ["A1", "A1", "A2"],
        "Level": "Debug"
    }
}

# Errors for fuzzywuzzy
HEAVY_ERROR = {
    "nme": 5,
    "do read": "1",
    "count": 42.0,
    "percentage": None,
    "extended": {
        "parameter": "A1",
        "set": ["A1", "A1", "A2"],
        "level": "dbg"
    }
}


NOFIX = {
    "nme": 5,
    "do read": "1",
    "count": 42.0,
    "percentage": None,
    "extended": {
        "parameter": "A1",
        "set": ["A1", "A1", "A2"],
        "level": "12345asdf"
    }
}


"""
Fixtures and helping functions
"""


@pytest.fixture(params=[Path("temp.yml"), Path("temp.json")])
def file(request):
    """
    Runs each test with a JSON file and a YAML file
    """
    yield request.param
    if request.param.exists():
        request.param.unlink()


def check_contents_match(parsed: Dict[str, Any], expected: Dict[str, Any]):
    """
    Ensures that the values of the parsed configuration matches whats expected
    :param parsed: The loaded configuration file
    :param expected: The expected configuration file
    :return: True if everything matches, false otherwise
    """
    for key in expected.keys():
        # Handle nested dictionaries
        if isinstance(expected[key], dict):
            check_contents_match(parsed[key], expected[key])

        # Handle lists
        elif isinstance(expected[key], list):
            for value in expected[key]:
                if value not in parsed[key]:
                    assert f"{value} not in {parsed[key]}"

        elif parsed[key] != expected[key]:
            assert f"{parsed[key]} does not match {expected[key]}"


"""
Data with bad spelling
"""


@pytest.mark.skipif(NO_FUZ, reason="fuzzywuzzy needed for this test to pass")
def test_fuzzy_wuzzy_works():
    choices = ["Debug", "Info", "Error"]
    results = fuzzywuzzy.process.extractOne("dbug", choices)
    if results[1] >= 75:
        if results[0] != "Debug":
            assert f"Did not find the correct value: {results!r}"
        assert f"Confidence level is too low: {results!r}"


@pytest.mark.skipif(NO_FUZ, reason="fuzzywuzzy needed for this test to pass")
def test_reading_and_writing_broken_configuration(file):
    configuration.write(file, HEAVY_ERROR)
    parsed = configuration.parse(file, TEMPLATE)
    check_contents_match(parsed, CONFIGURATION2)


@pytest.mark.skipif(NO_FUZ, reason="fuzzywuzzy needed for this test to pass")
def test_uncorrectable_configuration(file):
    configuration.write(file, NOFIX)

    with pytest.raises(ValueError):
        parsed = configuration.parse(file, TEMPLATE)
        check_contents_match(parsed, CONFIGURATION2)


"""
Writing and reading basic configuration files without spelling errors
"""


def test_reading_and_writing_perfect_configuration(file):
    configuration.write(file, CONFIGURATION1)
    parsed = configuration.parse(file, TEMPLATE)
    check_contents_match(parsed, CONFIGURATION1)


def test_reading_and_writing_configuration_with_minor_issues(file):
    configuration.write(file, LIGHT_ERROR)
    parsed = configuration.parse(file, TEMPLATE)
    check_contents_match(parsed, CONFIGURATION2)


"""
Bad data
"""


def test_load_bad_data_file():
    file = Path("temp.txt")

    # Make some noise
    with file.open("w") as stream:
        stream.write("\\ # this is a bad file.\n\n\n 42")

    with pytest.raises(ValueError):
        configuration.parse(file)

    file.unlink()


def test_unknown_template_type():
    file = Path("temp.txt")

    configuration.write(file, {"data": 1})
    template = {"data": Path}

    with pytest.raises(ValueError):
        configuration.parse(file, template)

    file.unlink()
