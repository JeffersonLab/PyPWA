import os

import pytest

from PyPWA.libs import data_handler
from PyPWA.initializers.configurator import option_tools


EXAMPLE_DATA = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/sv_test_data.tsv"
)


@pytest.fixture()
def parser():
    template = data_handler.DataParser.default_options
    options = {"enable cache": False}
    command = option_tools.CommandOptions(template, options)
    setup = data_handler.DataParser.setup(command)
    return setup.return_interface()


@pytest.fixture()
def iterator():
    template = data_handler.DataIterator.default_options
    options = {"fail": True}
    command = option_tools.CommandOptions(template, options)
    setup = data_handler.DataIterator.setup(command)
    return setup.return_interface()


def test_parser_reads_example(parser):
    data = parser.parse(EXAMPLE_DATA)
    assert data["ctAD"][2] == -0.265433


def test_iterator_reads_example(iterator):
    reader = iterator.return_reader(EXAMPLE_DATA)
    event1 = reader.next()
    event2 = reader.next()
    event3 = reader.next()
    reader.close()

    assert event1["ctAD"] == -0.265433
    assert event2["phiAD"] == 0.675771
    assert event3["QFactor"] == 0.888493
