from abc import ABC
from dataclasses import dataclass
from enum import Enum
from io import StringIO
from itertools import product

from .utilities import Symbols, Settings


class Side(Enum):
    White = 1
    Black = 2


class PieceType(Enum):
    Man = 1
    King = 2


@dataclass
class Square:
    x: int
    y: int

    @property
    def side(self):
        return Side.White if (self.x + self.y) % 2 == 0 else Side.Black

    @property
    def top(self):
        return Square(self.x - 1, self.y)

    @property
    def bottom(self):
        return Square(self.x + 1, self.y)

    @property
    def left(self):
        return Square(self.x, self.y - 1)

    @property
    def right(self):
        return Square(self.x, self.y + 1)

    @staticmethod
    def from_symbol(symbol: str) -> 'Square | None':
        """
        :param symbol: a string representation of a square that consist of lowercase letter representing row
                       and a digit representing column, e.g. a1, b3, c6
        :return: Square object or None if the string representation is invalid
        """
        try:
            x, y = symbol
            return Square(ord(x) - 97, int(y) - 1)
        except ValueError:
            return None

    def get_squares_to(self, other: 'Square') -> list['Square']:
        """
        :param other: other Square
        :return: a list of squares on a diagonal between current square (exclusive) and the other square (inclusive)
        """
        if abs(self.x - other.x) != abs(self.y - other.y):
            raise ValueError('Squares between can be only calculated between squares on the same diagonal')
        start_from_left = self.y <= other.y
        start_from_top = self.x <= other.x
        squares = []
        while other != self:
            squares.insert(0, other)
            other = Square(
                other.x - (1 if start_from_top else -1),
                other.y - (1 if start_from_left else -1)
            )
        return squares

    def get_diagonal_squares(self) -> set['Square']:
        """
        :param size: number of squares in a board's row
        :return: all squares that are on the same diagonal (i.e. it is possible for King to get there in one move)
        """
        squares = set()
        for direction in (1, 1), (1, -1), (-1, 1), (-1, -1):
            x_step, y_step = direction
            current = self
            while 0 <= current.x <= Settings.BoardSize - 1 and 0 <= current.y <= Settings.BoardSize - 1:
                squares.add(current)
                current = Square(current.x + x_step, current.y + y_step)
        squares.remove(self)
        return squares

    def get_neighbor_diagonal_squares(self, ) -> set['Square']:
        pass

    def __str__(self):
        x_fmt = chr(self.x + 97)
        y_fmt = self.y + 1
        return f'{x_fmt}{y_fmt}'

    def __hash__(self):
        return hash(self.__str__())


@dataclass
class Piece:
    type_: PieceType
    side: Side


@dataclass
class Move(ABC):
    piece: Piece
    from_sq: Square


@dataclass
class SimpleMove(Move):
    to_sq: Square


@dataclass
class CrownMove(Move):
    through: list[Square]


@dataclass
class Board:
    squares: dict[Square, Piece | None]

    @staticmethod
    def populate_initial_board() -> 'Board':
        squares = {Square(i, j): None for i, j in product(range(Settings.BoardSize), range(Settings.BoardSize))}
        for i in range(Settings.BoardSize):
            if i % 2 == 0:
                squares[Square(1, i)] = Piece(PieceType.Man, Side.White)
                squares[Square(Settings.BoardSize - 1, i)] = Piece(PieceType.Man, Side.Black)
            else:
                squares[Square(0, i)] = Piece(PieceType.Man, Side.White)
                squares[Square(Settings.BoardSize - 2, i)] = Piece(PieceType.Man, Side.Black)
        return Board(squares)

    @property
    def top_left_sq(self) -> Square:
        return Square(0, 0)

    @property
    def top_right_sq(self) -> Square:
        return Square(0, Settings.BoardSize - 1)

    @property
    def bottom_left_sq(self) -> Square:
        return Square(Settings.BoardSize - 1, 0)

    @property
    def bottom_right_sq(self) -> Square:
        return Square(Settings.BoardSize - 1, Settings.BoardSize - 1)

    @property
    def corners(self) -> list[Square]:
        return [
            self.top_left_sq,
            self.top_right_sq,
            self.bottom_left_sq,
            self.bottom_right_sq
        ]

    @property
    def possible_moves(self) -> list[Move]:
        moves = []
        # TODO
        return moves

    def dump(self, stream=None):
        if stream is None:
            stream = StringIO()
        for row in range(Settings.BoardSize):
            for col in range(Settings.BoardSize):
                sq = Square(row, col)
                piece = self.squares[sq]
                if not piece:
                    match sq.side:
                        case Side.White:
                            stream.write(Symbols.WhiteSquare + '\t')
                        case Side.Black:
                            stream.write(Symbols.BlackSquare + '\t')
                else:
                    match (piece.type_, piece.side):
                        case (PieceType.Man, Side.White):
                            stream.write(Symbols.WhiteMan + '\t')
                        case (PieceType.King, Side.White):
                            stream.write(Symbols.WhiteKing + '\t')
                        case (PieceType.Man, Side.Black):
                            stream.write(Symbols.BlackMan + '\t')
                        case (PieceType.King, Side.Black):
                            stream.write(Symbols.BlackKing + '\t')
            stream.write('\n')
