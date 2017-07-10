import os
import sys

import pytest

from PyPWA.initializers.configurator import options
from PyPWA.initializers.configurator.create_config import _level_processing

sys.path.append(os.path.join(
    os.path.dirname(__file__), "../../../data/source_files"
))

import simple_option_object


@pytest.fixture
def option():
    return simple_option_object.SimpleOptions


@pytest.fixture
def full_options(option):
    return _level_processing._FullOptions(option)


@pytest.fixture(params=full_options(option()).difficulties)
def full_options_difficulties(request):
    return request.param


def test_full_options_name(full_options):
    assert "SimpleOptions" == full_options.name


def test_full_option_plugin_options(full_options):
    assert "Option1" in full_options.plugin_options[full_options.name]
    assert "Option2" in full_options.plugin_options[full_options.name]
    assert "Option3" in full_options.plugin_options[full_options.name]


def test_full_option_difficulties_keys(full_options_difficulties):
    assert isinstance(full_options_difficulties[0], str)


def test_full_option_difficulties_values(full_options_difficulties):
    assert full_options_difficulties[1] in options.Levels


@pytest.fixture
def process_options():
    return _level_processing.ProcessOptions()


def test_process_options_required(process_options, option):
    processed = process_options.processed_options(
        option, options.Levels.REQUIRED
    )

    assert "Option1" in processed[option.plugin_name]
    assert "Option2" not in processed[option.plugin_name]
    assert "Option3" not in processed[option.plugin_name]


def test_process_options_optional(process_options, option):
    processed = process_options.processed_options(
        option, options.Levels.OPTIONAL
    )

    assert "Option1" in processed[option.plugin_name]
    assert "Option2" in processed[option.plugin_name]
    assert "Option3" not in processed[option.plugin_name]


def test_process_options_advanced(process_options, option):
    processed = process_options.processed_options(
        option, options.Levels.ADVANCED
    )

    assert "Option1" in processed[option.plugin_name]
    assert "Option2" in processed[option.plugin_name]
    assert "Option3" in processed[option.plugin_name]
