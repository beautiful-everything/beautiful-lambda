def require_lambda_base(x):
    if isinstance(x, LambdaBase):
        return x
    else:
        return Constant(x)


class LambdaBase:
    def __add__(self, other):
        return BinOp(self, require_lambda_base(other), lambda a, b: a + b)

    def __sub__(self, other):
        return BinOp(self, require_lambda_base(other), lambda a, b: a - b)

    def __mul__(self, other):
        return BinOp(self, require_lambda_base(other), lambda a, b: a * b)

    def __radd__(self, other):
        return require_lambda_base(other) + self

    def __rsub__(self, other):
        return require_lambda_base(other) - self

    def __rmul__(self, other):
        return require_lambda_base(other) * self

    def __call__(self, *args):
        return self.call(args, 0)

    def implicit_args_count(self):
        return 0

    def call(self, args, implicit_args_before):
        raise NotImplemented

    def is_positional(self):
        return None


class Argument(LambdaBase):
    def __init__(self, position=None):
        self.position = position

    def is_positional(self):
        return self.position is not None

    def implicit_args_count(self):
        return 0 if self.is_positional() else 1

    def call(self, args, implicit_args_before):
        if self.is_positional():
            pos = self.position
        else:
            pos = implicit_args_before

        if pos >= len(args):
            raise ValueError(
                'At least {} positional arguments were required, but {} was provided'.format(pos + 1, len(args)))
        return args[pos]


class Constant(LambdaBase):
    def __init__(self, value):
        self.value = value

    def call(self, args, implicit_args_before):
        return self.value


class BinOp(LambdaBase):
    def __init__(self, lhs, rhs, op):
        assert isinstance(lhs, LambdaBase)
        assert isinstance(rhs, LambdaBase)
        if lhs.is_positional() is None:
            self._is_positional = rhs.is_positional()
        else:
            self._is_positional = lhs.is_positional()
            # TODO Think of a more elegant way for this check
            if rhs.is_positional() is not None and \
                    lhs.is_positional() != rhs.is_positional():
                raise ValueError('You can\'t mix positional and implicit arguments')
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        self._implicit_args_count = self.lhs.implicit_args_count() + self.rhs.implicit_args_count()

    def is_positional(self):
        return self._is_positional

    def implicit_args_count(self):
        return self._implicit_args_count

    def call(self, args, implicit_args_before):
        return self.op(self.lhs.call(args, implicit_args_before),
                       self.rhs.call(args, implicit_args_before + self.lhs.implicit_args_count()))


_ = Argument(None)
_1, _2, _3, _4, _5, _6, _7, _8, _9 = [Argument(n) for n in range(9)]
