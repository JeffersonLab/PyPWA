import os
import logging

import numpy

import PyPWA.libs.data.memory.cache
import PyPWA.libs.data.file_manager

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

TEST_KV_DICT_FILE = os.path.join(os.path.dirname(__file__), "test_docs/kv_test_data.txt")


def test_cache_loop():  # I will think of a better way to do this eventually
    reader = PyPWA.libs.data.file_manager.MemoryInterface(False)
    data = reader.parse(TEST_KV_DICT_FILE)

    cache = PyPWA.libs.data.memory.cache.MemoryCache()
    cache.make_cache(data, TEST_KV_DICT_FILE)

    returned_data = cache.read_cache(TEST_KV_DICT_FILE)

    assert returned_data != False
    numpy.testing.assert_array_equal(data["ctAD"], returned_data["ctAD"])
