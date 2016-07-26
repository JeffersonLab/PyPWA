import os

import pytest
import numpy

from PyPWA.libs.data import traffic_cop


CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "test_docs/sv_test_data.csv"
)

GAMP_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "test_docs/gamp_test_data.gamp"
)

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__), "test_docs/temporary_write_data"
)
