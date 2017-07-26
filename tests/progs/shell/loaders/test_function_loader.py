import os

import pytest

from PyPWA.progs.shell import loaders

"""
Test Data
"""

FUNCTIONS_FOR_TEST = os.path.join(
    os.path.dirname(__file__),
    "../../../data/source_files/functions_without_math.py"
)


"""
Test simple function
"""

@pytest.fixture
def function_without_math():
    loader = loaders.FunctionLoader(
        FUNCTIONS_FOR_TEST, "processing", "setup"
    )
    return loader


def test_function_and_setup_return_true(function_without_math):
    processing = function_without_math.process
    setup = function_without_math.setup
    assert processing(1, 1)
    assert setup()


"""
Test with simpler function
"""

@pytest.fixture
def function_without_math_or_setup():
    loader = loaders.FunctionLoader(
        FUNCTIONS_FOR_TEST, "processing", "A dirty lie"
    )
    return loader


def test_function_without_setup_is_none(function_without_math_or_setup):
    setup = function_without_math_or_setup.setup
    assert isinstance(setup(), type(None))
