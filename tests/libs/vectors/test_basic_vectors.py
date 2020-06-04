import pytest
import numpy
import pandas

from PyPWA.libs import vectors

ARRAY_LENGTH = 20

@pytest.fixture()
def four_vector():
    v = vectors.FourVector(ARRAY_LENGTH)
    v.e = numpy.random.rand(ARRAY_LENGTH)
    v.x = numpy.random.rand(ARRAY_LENGTH)
    v.y = numpy.random.rand(ARRAY_LENGTH)
    v.z = numpy.random.rand(ARRAY_LENGTH)
    return v


@pytest.fixture()
def three_vector(four_vector):
    return four_vector.get_three_vector()


"""
Abstract Vector Tests
"""
# Test String

def test_four_vector_str(four_vector):
    assert str(four_vector)


# Test Magic Math

def test_four_vector_addition(four_vector):
    assert isinstance(four_vector + four_vector, vectors.FourVector)
    assert isinstance(four_vector + four_vector, vectors.FourVector)


def test_four_vector_subtraction(four_vector):
    assert isinstance(four_vector - four_vector, vectors.FourVector)


def test_four_vector_scalar_multiplication(four_vector):
    assert isinstance(four_vector * 2, vectors.FourVector)


# Test Iterators and length

def test_four_vector_len(four_vector):
    assert len(four_vector) == ARRAY_LENGTH


def test_four_vector_iterable(four_vector):
    for event in four_vector:
        assert isinstance(event, vectors.FourVector)


# Test setters and getters

def test_three_vector_can_not_set_energy(three_vector):
    with pytest.raises(AttributeError):
        three_vector.e = numpy.random.rand(ARRAY_LENGTH)


def test_three_vector_errors_with_different_size_array(three_vector):
    with pytest.raises(ValueError):
        three_vector.z = numpy.random.rand(ARRAY_LENGTH+1)


def test_four_vector_set_scalar(four_vector):
    vector = four_vector.get_copy()
    vector.e = 5
    for event in vector.e:
        assert event == 5


def test_three_vector_set_array(three_vector):
    vector = three_vector.get_copy()
    new_array = numpy.random.rand(ARRAY_LENGTH)
    vector.x = new_array
    numpy.testing.assert_array_equal(vector.x, new_array)


def test_four_vector_can_not_get_q(four_vector):
    with pytest.raises(AttributeError):
        four_vector.q


# Test Utilities

def test_three_vector_copy_is_real(three_vector):
    copy = three_vector.get_copy()
    copy.x = 5
    assert not (copy.x == three_vector.x).all()


def test_four_vector_get_array_returns_array(four_vector):
    assert isinstance(four_vector.dataframe, pandas.DataFrame)


def test_three_vector_splits(three_vector):
    for split in three_vector.split(4):
        assert isinstance(split, vectors.ThreeVector)


def test_dot_between_different_vector_types(four_vector, three_vector):
    with pytest.raises(ValueError):
        four_vector.get_dot(three_vector)


# Test Builtin Properties

def test_four_vector_length(four_vector):
    assert isinstance(four_vector.get_length(), numpy.ndarray)


def test_three_vector_theta(three_vector):
    assert isinstance(three_vector.get_theta(), numpy.ndarray)


def test_four_vector_phi(four_vector):
    assert isinstance(four_vector.get_phi(), numpy.ndarray)


def test_three_vector_sin_theta(three_vector):
    assert isinstance(three_vector.get_sin_theta(), numpy.ndarray)


def test_four_vector_cos_theta(four_vector):
    assert isinstance(four_vector.get_cos_theta(), numpy.ndarray)


def test_three_vector_setters(three_vector):
    vector = three_vector.get_copy()
    vector.x = 3
    vector.y = 2
    vector.z = 1
    x = (vector.x == 3).all()
    y = (vector.y == 2).all()
    z = (vector.z == 1).all()
    assert x and y and z


"""
Four and Three Vector Tests
"""
# Test Cross Multiplication

def test_four_vector_cross_multiplication(four_vector):
    with pytest.raises(ValueError):
        four_vector * four_vector


def test_three_vector_multiplication(three_vector):
    assert isinstance(three_vector * three_vector, vectors.ThreeVector)


# Test Dot Multiplication

def test_four_vector_dot(four_vector):
    assert isinstance(four_vector.get_dot(four_vector), numpy.ndarray)


def test_three_vector_dot(three_vector):
    assert isinstance(three_vector.get_dot(three_vector), numpy.ndarray)


# Test Representation

def test_four_vector_repr(four_vector):
    assert isinstance(repr(four_vector), str)


def test_three_vector_repr(three_vector):
    assert isinstance(repr(three_vector), str)


# Test Length Squared

def test_three_vector_length_squared(three_vector):
    assert isinstance(three_vector.get_length_squared(), numpy.ndarray)


def test_four_vector_length_squared(four_vector):
    assert isinstance(four_vector.get_length_squared(), numpy.ndarray)
