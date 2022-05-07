from abc import ABC
from dataclasses import dataclass
from enum import Enum
from io import StringIO
from itertools import product

from .utilities import Symbols


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
        try:
            x, y = symbol
            return Square(ord(x) - 97, int(y) - 1)
        except ValueError:
            return None

    def get_squares_to(self, other: 'Square') -> list['Square']:
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
    size: int

    @staticmethod
    def populate_initial_board(size: int) -> 'Board':
        squares = {Square(i, j): None for i, j in product(range(size), range(size))}
        for i in range(size):
            if i % 2 == 0:
                squares[Square(1, i)] = Piece(PieceType.Man, Side.White)
                squares[Square(size - 1, i)] = Piece(PieceType.Man, Side.Black)
            else:
                squares[Square(0, i)] = Piece(PieceType.Man, Side.White)
                squares[Square(size - 2, i)] = Piece(PieceType.Man, Side.Black)
        return Board(squares, size)

    @property
    def top_left_sq(self) -> Square:
        return Square(0, 0)

    @property
    def top_right_sq(self) -> Square:
        return Square(0, self.size - 1)

    @property
    def bottom_left_sq(self) -> Square:
        return Square(self.size - 1, 0)

    @property
    def bottom_right_sq(self) -> Square:
        return Square(self.size - 1, self.size - 1)

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
        for row in range(self.size):
            for col in range(self.size):
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
