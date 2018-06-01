class Lambda:

    def __init__(self, lmbda):
        self.lmbda = lmbda

    def __add__(self, other):
        return Lambda(lambda *args, **kwargs: self.lmbda(*args, **kwargs) + other)

    def __radd__(self, other):
        return Lambda(lambda *args, **kwargs: other + self.lmbda(*args, **kwargs))

    def __call__(self, *args, **kwargs):
        return self.lmbda(*args, **kwargs)


_ = Lambda(lambda x: x)

if __name__ == '__main__':
    l = [1, 2, 3, 4]
    print(list(map(_ + 5, l)))
    print(list(map(1 + _, l)))
