import pytest

import rubric
from rubric import *


def test_int():
    schema = Int()
    schema.validate(1)
    rubric.validate(schema, 1)

    with pytest.raises(ValidateError):
        schema.validate('1')


def test_int1():
    rubric.validate(Int(), 1)

    with pytest.raises(ValidateError):
        rubric.validate(Int(), '1')


def test_int2():
    rubric.validate(int, 1)

    with pytest.raises(ValidateError):
        rubric.validate(Int(), '1')


def test_float():
    schema = Float()
    schema.validate(1.0)

    with pytest.raises(ValidateError):
        schema.validate('1')


def test_str():
    schema = Str()
    schema.validate('1')

    with pytest.raises(ValidateError):
        schema.validate(1)


def test_bytes():
    schema = Bytes()
    schema.validate(b'1')

    with pytest.raises(ValidateError):
        schema.validate('1')


def test_bool():
    schema = Bool()
    schema.validate(True)

    with pytest.raises(ValidateError):
        schema.validate('1')


def test_none():
    schema = Null()
    schema.validate(None)

    with pytest.raises(ValidateError):
        schema.validate('1')
