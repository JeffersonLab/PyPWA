from PyPWA.libs import initial_logging


def test_initial_logging_takes_a_logging_level():
    initial_logging.setup_logging(9001)
