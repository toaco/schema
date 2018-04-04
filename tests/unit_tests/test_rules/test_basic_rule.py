import pytest

from rubric import *


def test_int():
    schema = Int(validator=lambda x: x < 10)
    schema.validate(1)

    with pytest.raises(ValidateError):
        schema.validate(10)


def test_set_error_properly():
    schema = Int(validator=lambda x: x < 10)
    with pytest.raises(ValidateError) as exc_info:
        schema.validate(10)

    assert exc_info.value == ValidateError()

    schema = Int(validator=lambda x: x < 10, error='ERROR')
    with pytest.raises(ValidateError) as exc_info:
        schema.validate(10)

    assert exc_info.value == ValidateError('ERROR')
