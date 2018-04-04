from .exc import ValidateError


def validate(schema, ins):
    """验证模式和对象是否匹配
    
    :param schema:模式，可以是一个类名，Schema对象(只要有validate方法就可以)，可包装对象或者
    其他Python对象
    :param ins:待验证的对象
    """
    if isinstance(schema, type):
        # schema是一个类，此时判断类型是否符合即可
        if not isinstance(ins, schema):
            raise ValidateError('{} is not instance of {}'.format(
                ins, str(schema)))
    else:
        if hasattr(schema, 'validate'):
            # Schema是一个Schema对象,此时调用Schema的validate方法进行判断
            assert callable(schema.validate)
            schema.validate(ins)
        else:
            raw_schema = schema
            schema_type = type(raw_schema)
            collection_schema = {
                dict: Dict,
                tuple: Tuple,
                list: List,
                set: Set,
            }
            if schema_type in collection_schema:
                # 有包装类型的对象,这里的特例是int,float等对象虽然也有包装类型，但是可以将其直接
                # 作为其他对象进行比较，避免不必要的包装
                schema = collection_schema[schema_type](raw_schema)
                schema.validate(ins)
            else:
                # 其他对象，直接比较
                if schema != ins:
                    raise ValidateError


_default = object()  # 可用做方法参数的默认值，从而判断用户是否传递了该参数


class Schema(object):
    """
    Schema类用于构造一个模板，之后可基于该模板验证对象，转换对象或者生成对象，对应的方法分别为：
    validate,convert和generate．

    :param schema: 模式
    :param validator: 验证器
    :param error: 未通过验证时默认的错误消息
    :param default: 未通过验证时的默认值
    """

    type = None  # 子类必须设置该值，该值在`Schema．validate`方法中用来判断类型是否正确

    def __init__(self, schema=None, validator=None, error=None,
                 default=_default):
        self._schema = schema
        self._validator = validator
        self._error = error
        self.default = default

    def validate(self, ins):
        """
        验证一个对象是否符合该模式，该方法根据类的type变量进行类型判断，子类可以重载该方法实现
        自定义的验证规则．
        
        如果验证失败，则抛出ValidateError异常，其消息可通过error属性配置．对于验证失败的值，如果
        设置了default属性，那么将不会抛出异常．
        
        :param ins: 待验证的对象
        """
        if not isinstance(ins, self.type):
            raise ValidateError(
                '{} is not instance of {}'.format(ins, str(self.type)))

        if self._validator:
            if not self._validator(ins):
                raise ValidateError(
                    self._error) if self._error else ValidateError()
        return ins

    def convert(self, ins):
        pass

    def generate(self, ins):
        pass


class Int(Schema):
    type = int


class Float(Schema):
    type = float


class Str(Schema):
    type = str


class Bytes(Schema):
    type = bytes


class Bool(Schema):
    type = bool


class Null(Schema):
    type = type(None)


class Tuple(Schema):
    type = tuple


_builtin_types = (int, str, bytes, list, dict, set)


class List(Schema):
    type = list

    def __init__(self, schema=None, pattern='*', validator=None, error=None,
                 default=_default):
        super().__init__(schema, validator, error, default)
        self._pattern = pattern

    def validate(self, ins):
        super().validate(ins)
        if self._schema is None:
            return

        if self._pattern == '*':
            self._handle_default(ins)

    def _handle_default(self, ins):
        if not self._schema:
            if ins:
                raise ValidateError('')
        else:
            # 只能有一个元素
            assert len(self._schema) == 1
            element = self._schema[0]
            for v in ins:
                validate(element, v)


class Dict(Schema):
    type = dict

    def __init__(self, schema=None, policy='default', validator=None,
                 error=None, default=_default):
        super().__init__(schema, validator, error, default)
        self._policy = policy

    def validate(self, ins: dict):
        super().validate(ins)
        if self._schema is None:
            return

        if self._policy == 'default':
            self._handle_default(ins)

    def _handle_default(self, ins):
        # 不允许出现schema定义之外的
        o_s = {*ins.keys()} - {*self._schema.keys()}
        if o_s:
            raise ValidateError

        for k, v in self._schema.items():
            if isinstance(k, _builtin_types):
                if k in ins:
                    validate(v, ins[k])
                else:
                    if isinstance(v, Schema) and v.default is not _default:
                        pass
                    else:
                        raise ValidateError('没有默认值')


class Set(Schema):
    type = set
