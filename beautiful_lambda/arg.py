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

    def call(self, args):
        raise NotImplemented

    def __call__(self, *args):
        return self.call(args)


class Argument(LambdaBase):
    def __init__(self, position=None):
        self.position = position

    def is_positional(self):
        return self.position is not None

    def call(self, args):
        if not self.is_positional():
            raise NotImplemented
        if self.position >= len(args):
            raise ValueError(
                'At least {} positional arguments were required, but {} was provided'
                    .format(self.position + 1, len(args)))
        return args[self.position]


class Constant(LambdaBase):
    def __init__(self, value):
        self.value = value

    def call(self, args):
        return self.value


class BinOp(LambdaBase):
    def __init__(self, lhs, rhs, op):
        assert isinstance(lhs, LambdaBase)
        assert isinstance(rhs, LambdaBase)
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def call(self, args):
        return self.op(self.lhs.call(args), self.rhs.call(args))


_ = Argument(None)
_1, _2, _3, _4, _5, _6, _7, _8, _9 = [Argument(n) for n in range(9)]
