import pytest

import rubric
from rubric import *


def test_nest_dict():
    # 简单的嵌套
    schema = {
        'a': int,
        'b': str,
        'c': {
            'c1': Int(validator=lambda x: x < 10)
        }
    }

    rubric.validate(schema, {
        'a': 1,
        'b': '2',
        'c': {
            'c1': 3
        }
    })

    with pytest.raises(ValidateError):
        rubric.validate(schema, {
            'a': 1,
            'b': '2',
            'c': {
                'c1': 11
            }
        })


def test_nest_dict1():
    # 不可以多键
    schema = {
        'a': int,
        'b': str
    }

    with pytest.raises(ValidateError):
        rubric.validate(schema, {
            'a': 1,
            'b': '2',
            'c': 1
        })


def test_nest_dict2():
    # 可少键，但是必须提供默认值
    schema = {
        'a': int,
        'b': str
    }

    with pytest.raises(ValidateError):
        rubric.validate(schema, {
            'a': 1,
        })

    schema = {
        'a': int,
        'b': Str(default='1')
    }

    rubric.validate(schema, {
        'a': 1
    })


def test_nest_dict3():
    # 　嵌套更深
    schema = {
        'a': int,
        'b': str,
        'c': {
            'c1': Int(validator=lambda x: x < 10),
            'd': {
                'd1': Int(validator=lambda x: x < 10)
            }
        }
    }

    rubric.validate(schema, {
        'a': 1,
        'b': '2',
        'c': {
            'c1': 3,
            'd': {
                'd1': 9
            }
        }
    })

    with pytest.raises(ValidateError):
        rubric.validate(schema, {
            'a': 1,
            'b': '2',
            'c': {
                'c1': 3,
                'd': {
                    'd1': 11
                }
            }
        })


def test_dict_list():
    # 字典和列表
    schema = {
        'a': [],
        'b': [
            {
                'c': int,
                'd': 3,
                'e': [9]
            }
        ]
    }

    rubric.validate(schema, {
        'a': [],
        'b': [
            {
                'c': 1,
                'd': 3,
                'e': [9]

            }
        ]
    })

    rubric.validate(schema, {
        'a': [],
        'b': [
            {
                'c': 1,
                'd': 3,
                'e': [9, 9]

            }
        ]
    })

    with pytest.raises(ValidateError):
        rubric.validate(schema, {
            'a': [1],
            'b': [
                {
                    'c': 1,
                    'd': 3,
                    'e': [9]
                }
            ]
        })

    with pytest.raises(ValidateError):
        rubric.validate(schema, {
            'a': [],
            'b': [
                {
                    'c': 1,
                    'd': 3,
                    'e': [8]
                }
            ]
        })
