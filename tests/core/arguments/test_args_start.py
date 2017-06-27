import sys

import pytest

from PyPWA.core.arguments import start


@pytest.fixture()
def patch_args(monkeypatch):
    holds = sys.argv
    args = ['RougeTest', '--option1', '123', '--option2', 'a_string']
    monkeypatch.setattr('sys.argv', args)
    yield
    monkeypatch.setattr('sys.argv', holds)


@pytest.fixture()
def initializer(patch_args):
    return start.StartArguments()


def test_blank_module(initializer):
    initializer.start('blank shell module', 'Quick Test')
