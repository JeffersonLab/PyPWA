import collections
import os

import numpy
import pytest

from PyPWA.libs.components.data_processor import shell_interface

CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/sv_test_data.csv"
)

GAMP_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/gamp_test_data.gamp"
)

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/temporary_write_data"
)


#
