import unittest

from ..models import *

from ..utilities import Settings


class TestSquare(unittest.TestCase):
    def setUp(self) -> None:
        Settings.BoardSize = 4

    def test_from_symbol_1(self):
        self.assertEqual(Square(0, 0), Square.from_symbol('a1'))

    def test_from_symbol_2(self):
        self.assertEqual(Square(7, 7), Square.from_symbol('h8'))

    def test_from_symbol_3(self):
        self.assertEqual(Square(1, 1), Square.from_symbol('b2'))

    def test_from_symbol_4(self):
        self.assertEqual(Square(3, 5), Square.from_symbol('d6'))

    def test_side_1(self):
        self.assertEqual(Side.White, Square(0, 0).side)

    def test_side_2(self):
        self.assertEqual(Side.Black, Square(0, 1).side)

    def test_side_3(self):
        self.assertEqual(Side.Black, Square(1, 0).side)

    def test_side_4(self):
        self.assertEqual(Side.White, Square(1, 1).side)

    def test_direction_top(self):
        self.assertEqual(Square(1, 3), Square(2, 3).top)

    def test_direction_right(self):
        self.assertEqual(Square(4, 6), Square(4, 5).right)

    def test_direction_left(self):
        self.assertEqual(Square(1, 2), Square(1, 3).left)

    def test_direction_bottom(self):
        self.assertEqual(Square(7, 6), Square(6, 6).bottom)

    def test_squares_to_bottom_right(self):
        self.assertEqual(
            [
                Square(3, 4),
                Square(4, 5),
                Square(5, 6)
            ],
            Square(2, 3).get_squares_to(Square(5, 6))
        )

    def test_squares_to_bottom_left(self):
        self.assertEqual(
            [
                Square(2, 1),
                Square(3, 0)
            ],
            Square(1, 2).get_squares_to(Square(3, 0))
        )

    def test_squares_to_top_left(self):
        self.assertEqual(
            [
                Square(6, 4),
                Square(5, 3),
                Square(4, 2),
                Square(3, 1),
                Square(2, 0)
            ],
            Square(7, 5).get_squares_to(Square(2, 0))
        )

    def test_squares_to_top_right(self):
        self.assertEqual(
            [
                Square(3, 6),
                Square(2, 7)
            ],
            Square(4, 5).get_squares_to(Square(2, 7))
        )

    def test_squares_same(self):
        self.assertEqual(
            [],
            Square(4, 5).get_squares_to(Square(4, 5))
        )

    def test_diagonal_squares_1(self):
        self.assertEqual(
            {
                Square(1, 1),
                Square(2, 2),
                Square(3, 3)
            },
            Square(0, 0).get_diagonal_squares()
        )

    def test_diagonal_squares_2(self):
        self.assertEqual(
            {
                Square(0, 0),
                Square(1, 1),
                Square(2, 2)
            },
            Square(3, 3).get_diagonal_squares()
        )

    def test_diagonal_squares_3(self):
        self.assertEqual(
            {
                Square(3, 3),
                Square(1, 1),
                Square(0, 0),
                Square(3, 1),
                Square(1, 3)
            },
            Square(2, 2).get_diagonal_squares()
        )
