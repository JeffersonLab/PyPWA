import logging

functions_logger = logging.getLogger(__name__)


def processing(values, parameters):
    final = values['x'] / values['y']
    final = final * (['z'] + parameters['A'])
    return final


def setup():
    functions_logger.info("Setup was called")
