# coding=utf-8

import pytest

from PyPWA.libs import configuration_db


@pytest.fixture(scope="function", autouse=True)
def clear_configuration():
    with pytest.warns(RuntimeWarning):
        configuration_db.Connector().purge()
