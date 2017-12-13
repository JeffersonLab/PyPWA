import numpy
import pytest

from PyPWA.libs.components.process import _data_split

TWO_SPLIT = _data_split.SetupData(2)
FOUR_SPLIT = _data_split.SetupData(4)

"""
Test Array Split
"""

ARRAY = {"data": numpy.random.rand(50)}


@pytest.fixture(params=[TWO_SPLIT, FOUR_SPLIT])
def split_array(request):
    return request.param.split(ARRAY)


def sum_array_splits(splits):
    total = numpy.float64(0)
    for packet in splits:
        total += numpy.sum(packet['data'])
    return total


def test_array_sum_matches(split_array):
    numpy.testing.assert_approx_equal(
        sum_array_splits(split_array), numpy.sum(ARRAY['data'])
    )


def test_array_four_split_is_four():
    assert len(FOUR_SPLIT.split(ARRAY)) == 4


def test_array_two_split_is_two():
    assert len(TWO_SPLIT.split(ARRAY)) == 2


"""
Test List Split
"""

FAIL_LIST = {"data": ["FAIL"]}
LIST = {"data": ["123","234","345","456"]}


@pytest.fixture(params=[TWO_SPLIT, FOUR_SPLIT])
def split_list(request):
    return request.param.split(LIST)


def test_list_has_correct_values(split_list):
    for a_list in split_list:
        for value in a_list['data']:
            assert value in ("123","234","345","456")


def test_four_split_list_is_four():
    assert len(FOUR_SPLIT.split(LIST)) == 4


def test_two_split_list_is_two():
    assert len(TWO_SPLIT.split(LIST)) == 2


def test_list_split_fails_if_too_small():
    with pytest.raises(ValueError):
        TWO_SPLIT.split(FAIL_LIST)


"""
Test Unknown Data
"""

def test_unknown_data_raises_error():
    with pytest.raises(ValueError):
        TWO_SPLIT.split({"data":"A failure of a string"})
