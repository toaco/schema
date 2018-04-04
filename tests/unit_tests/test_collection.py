import pytest

import rubric
from rubric import *


def test_dict():
    schema = Dict()
    schema.validate({})
    schema.validate({1: 2})
    rubric.validate(schema, {1: 2})

    with pytest.raises(ValidateError):
        schema.validate('1')


def test_dict1():
    schema = Dict({1: str})
    schema.validate({1: '1'})

    with pytest.raises(ValidateError):
        schema.validate({1: 1})


def test_list():
    # 无模式
    schema = List()
    schema.validate([])
    schema.validate([1, 2, 3])

    with pytest.raises(ValidateError):
        schema.validate('1')


def test_list1():
    # 有模式,使用默认匹配模式＊
    schema = List([1])
    schema.validate([])
    schema.validate([1])
    schema.validate([1, 1])

    with pytest.raises(ValidateError):
        schema.validate([2])

    with pytest.raises(ValidateError):
        schema.validate([1, 2])
