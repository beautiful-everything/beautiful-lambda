import unittest

from beautiful_lambda import _1, _2, _3


class SingleArgTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(list(map(_1 + 2, [1, 2, 3, 4])), [3, 4, 5, 6])
        self.assertEqual(list(map(_1 + 'x', ['a', 'b', 'c', 'd'])), ['ax', 'bx', 'cx', 'dx'])

    def test_radd(self):
        self.assertEqual(list(map(2 + _1, [1, 2, 3, 4])), [3, 4, 5, 6])
        self.assertEqual(list(map('x' + _1, ['a', 'b', 'c', 'd'])), ['xa', 'xb', 'xc', 'xd'])

    def test_expression(self):
        self.assertEqual((_3 - 2 + (_2 * _1 + 1))(1, 2, 3), 4)
