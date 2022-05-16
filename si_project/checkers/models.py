import copy
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from functools import cached_property, cache
from io import StringIO
from itertools import product

from .utilities import Symbols, Settings


class Side(Enum):
    White = 1
    Black = 2

    @property
    def next(self):
        if self == Side.White:
            return Side.Black
        else:
            return Side.White


class PieceType(Enum):
    Man = 1
    King = 2


class SquareUtilities:
    @staticmethod
    @cache
    def side(x, y):
        return Side.White if (x + y) % 2 == 0 else Side.Black

    @staticmethod
    @cache
    def top(x, y):
        return Square(x - 1, y)

    @staticmethod
    @cache
    def bottom(x, y):
        return Square(x + 1, y)

    @staticmethod
    @cache
    def left(x, y):
        return Square(x, y - 1)

    @staticmethod
    @cache
    def right(x, y):
        return Square(x, y + 1)

    @staticmethod
    @cache
    def sector_multiplier(x, y):
        if 2 <= x <= 5 and 2 <= y <= 5:
            return 7
        elif 1 <= x <= 6 and 1 <= y <= 6:
            return 6
        else:
            return 5

    @staticmethod
    @cache
    def get_squares_to(x, y, other: 'Square') -> list['Square']:
        """
        :param other: other Square
        :return: a list of squares on a diagonal between current square (exclusive) and the other square (inclusive)
        """
        if abs(x - other.x) != abs(y - other.y):
            raise ValueError('Squares between can be only calculated between squares on the same diagonal')
        start_from_left = y <= other.y
        start_from_top = x <= other.x
        squares = []
        while other.x != x or other.y != y:
            squares.insert(0, other)
            other = Square(
                other.x - (1 if start_from_top else -1),
                other.y - (1 if start_from_left else -1)
            )
        return squares

    @staticmethod
    @cache
    def diagonal_squares(x, y) -> set['Square']:
        """
        :return: set of squares that are on the same diagonal (i.e. it is possible for King to get there in one move)
        """
        squares = set()
        for direction in (1, 1), (1, -1), (-1, 1), (-1, -1):
            x_step, y_step = direction
            current_x, current_y = x, y
            while 0 <= current_x <= Settings.BoardSize - 1 and 0 <= current_y <= Settings.BoardSize - 1:
                squares.add(Square(current_x, current_y))
                current_x, current_y = current_x + x_step, current_y + y_step
        squares.remove(Square(x, y))
        return squares

    @staticmethod
    @cache
    def neighbours(x, y) -> set['Square']:
        """
        :return: set of squares that are on the same diagonal and are direct neigbours of current square
        """
        return {s for s in Square(x, y).diagonal_squares if abs(x - s.x) == 1 and abs(y - s.y) == 1}

    @staticmethod
    @cache
    def neighbours_with_subsequent(x, y) -> set[tuple['Square', 'Square']]:
        """
        :return: set of pairs (neighbour, neighbour of a neighbour on the same diagonal) squares,
                 i.e. where would a crowning take place and where would a Man go after crowning
        """
        squares = set()
        for direction in (2, 2), (2, -2), (-2, 2), (-2, -2):
            x_step, y_step = direction
            if 0 <= x + x_step <= Settings.BoardSize - 1 and 0 <= y + y_step <= Settings.BoardSize - 1:
                squares.add((
                    Square(x + int(x_step / 2), y + int(y_step / 2)),
                    Square(x + x_step, y + y_step)
                ))
        return squares

    @staticmethod
    @cache
    def get_forward_neighbours(x, y, side: Side) -> set['Square']:
        """
        :param side: side used as a reference
        :return: list of neigbour diagonal squares that are "in front" given a side (white or black)
        """
        x_diff = -1 if side == Side.Black else 1
        return {s for s in Square(x, y).diagonal_squares if x - s.x == x_diff and abs(y - s.y) == 1}


@dataclass
class Square:
    x: int
    y: int

    @cached_property
    def side(self):
        return SquareUtilities.side(self.x, self.y)

    @cached_property
    def top(self):
        return SquareUtilities.top(self.x, self.y)

    @cached_property
    def bottom(self):
        return SquareUtilities.bottom(self.x, self.y)

    @cached_property
    def left(self):
        return SquareUtilities.left(self.x, self.y)

    @cached_property
    def right(self):
        return SquareUtilities.right(self.x, self.y)

    @cached_property
    def sector_multiplier(self):
        return SquareUtilities.sector_multiplier(self.x, self.y)

    @staticmethod
    @cache
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

    @cache
    def get_squares_to(self, other: 'Square') -> list['Square']:
        """
        :param other: other Square
        :return: a list of squares on a diagonal between current square (exclusive) and the other square (inclusive)
        """
        return SquareUtilities.get_squares_to(self.x, self.y, other)

    @property
    def diagonal_squares(self) -> set['Square']:
        """
        :return: set of squares that are on the same diagonal (i.e. it is possible for King to get there in one move)
        """
        return SquareUtilities.diagonal_squares(self.x, self.y)

    @property
    def neighbours(self) -> set['Square']:
        """
        :return: set of squares that are on the same diagonal and are direct neigbours of current square
        """
        return SquareUtilities.neighbours(self.x, self.y)

    @property
    def neighbours_with_subsequent(self) -> set[tuple['Square', 'Square']]:
        """
        :return: set of pairs (neighbour, neighbour of a neighbour on the same diagonal) squares,
                 i.e. where would a crowning take place and where would a Man go after crowning
        """
        return SquareUtilities.neighbours_with_subsequent(self.x, self.y)

    def get_forward_neighbours(self, side: Side) -> set['Square']:
        """
        :param side: side used as a reference
        :return: list of neigbour diagonal squares that are "in front" given a side (white or black)
        """
        return SquareUtilities.get_forward_neighbours(self.x, self.y, side)

    def __str__(self):
        x_fmt = chr(self.x + 97)
        y_fmt = self.y + 1
        return f'{x_fmt}{y_fmt}'

    def __hash__(self):
        return hash((self.x, self.y))


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

    def __str__(self):
        return f'{self.from_sq.__str__()} -> {self.to_sq.__str__()}'

    def __hash__(self):
        return hash(self.__str__())


@dataclass
class CrownMove(Move):
    through: list[Square]

    @property
    def to_sq(self) -> Square:
        return self.through[-1]

    def get_move_until(self, square: Square) -> 'CrownMove':
        prev_steps = []
        for step in self.through:
            prev_steps.append(step)
            if step == square:
                break
        return CrownMove(self.piece, self.from_sq, prev_steps)

    def __str__(self):
        return ' -> '.join([sq.__str__() for sq in [self.from_sq] + self.through]) + ' (bicie!)'

    def __hash__(self):
        return hash(self.__str__())


class Board:
    squares: dict[Square, Piece | None]
    moves: list[Move]

    def __init__(self, squares: dict[Square, Piece | None], moves: list[Move] = None):
        self.squares = squares
        self.moves = moves or []

    def to_num_repr(self):
        arr = []
        for square, piece in self.squares.items():
            if piece:
                color = 0 if piece.side == Side.White else 1
                type_ = 0 if piece.type_ == PieceType.Man else 1
                arr.append((square.x, square.y, color, type_))
        return tuple(arr)

    def from_num_repr(self, arr):
        board = Board({Square(i, j): None for i, j in product(range(8), range(8))})
        for i, j, color, type_ in arr:
            color = Side.White if color == 0 else Side.Black
            type_ = PieceType.Man if type_ == 0 else PieceType.King
            board.squares[Square(i, j)] = Piece(type_, color)
        return board

    @staticmethod
    def populate_initial_board() -> 'Board':
        squares = {Square(i, j): None for i, j in product(range(Settings.BoardSize), range(Settings.BoardSize))}
        for i in range(Settings.BoardSize):
            if i % 2 == 0:
                squares[Square(1, i)] = Piece(PieceType.Man, Side.Black)
                squares[Square(Settings.BoardSize - 1, i)] = Piece(PieceType.Man, Side.White)
            else:
                squares[Square(0, i)] = Piece(PieceType.Man, Side.Black)
                squares[Square(Settings.BoardSize - 2, i)] = Piece(PieceType.Man, Side.White)
        return Board(squares)

    @property
    def rating(self) -> int:
        """
        :return: Rating of the state of the game.
                 Absolute value of rating is a measure of unevenness of the game, where 0 means an completely even game
                    and 100 means an completely uneven game (a state of winning of one of the players).
                 Sign of rating indicates which side has advantage. A positive number means that the white player has
                    advantage and a negative number means that the black player has advantage.
        """

        if not [piece for piece in self.squares.values() if
                piece and piece.side == Side.White] or not self.get_possible_moves_of_side(Side.White):
            return -100
        elif not [piece for piece in self.squares.values() if
                  piece and piece.side == Side.Black] or not self.get_possible_moves_of_side(Side.Black):
            return 100
        else:
            sq_with_white_pieces = (square for square, piece in self.squares.items() if
                                    piece and piece.side == Side.White)
            sq_with_black_pieces = (square for square, piece in self.squares.items() if
                                    piece and piece.side == Side.Black)
            return sum(sq.sector_multiplier for sq in sq_with_white_pieces) - sum(
                sq.sector_multiplier for sq in sq_with_black_pieces)

    @property
    def is_in_draw_state(self) -> bool:
        return len(self.moves) >= 15 \
               and not any([piece.type_ == PieceType.Man for piece in self.squares.values()]) \
               and sum((1 if p.side == Side.White else -1 for p in self.squares.values())) == 0 \
               and all([isinstance(move, SimpleMove) for move in self.moves[:-15]])

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

    def _move(self, from_sq: Square | str, to_sq: Square | str) -> None:
        """
        Base method for moving a piece from square to square without game rules validation.
        Throws ValueError only in following cases:
        - Moving from or to non-existent square
        - Moving to already occupied square or from empty square
        """
        if isinstance(from_sq, str):
            from_sq = Square.from_symbol(from_sq)
        if isinstance(to_sq, str):
            to_sq = Square.from_symbol(to_sq)

        if from_sq not in self.squares:
            raise ValueError(f'{from_sq} square does not exist, but it was attempted to move piece from it')
        if to_sq not in self.squares:
            raise ValueError(f'{to_sq} square does not exist, but it was attempted to move piece to it')
        if not self.squares[from_sq]:
            raise ValueError(f'{from_sq} is empty, but it was attempted to move piece from it')
        if self.squares[to_sq]:
            raise ValueError(f'{to_sq} is occupied, but it was attempted to move piece to it')

        piece = self.squares[from_sq]
        self.squares[from_sq] = None
        self.squares[to_sq] = piece

    def _crown(self, sq: Square | str) -> None:
        """
        Base method for crowning, i.e. removing a piece from specified square without game rules validation.
        Throws ValueError only in case of non-existent or empty square.
        """
        if isinstance(sq, str):
            sq = Square.from_symbol(sq)

        if sq not in self.squares:
            raise ValueError(f'{sq} does not exist, but it was attempted to be crowned')
        if not self.squares[sq]:
            raise ValueError(f'{sq} is empty, but it was attempted to be crowned')
        self.squares[sq] = None

    def _promote(self, sq: Square | str) -> None:
        """
        Base method for promoting, i.e. upgrading a piece to a King.
        Throws ValueError only in case of non-existent or empty square or already King.
        """
        if isinstance(sq, str):
            sq = Square.from_symbol(sq)

        if sq not in self.squares:
            raise ValueError(f'{sq} does not exist, but it was attempted to be crowned')
        if not self.squares[sq]:
            raise ValueError(f'{sq} is empty, but it was attempted to be crowned')
        if self.squares[sq].type_ == PieceType.King:
            raise ValueError(f'{sq} has already King')
        self.squares[sq].type_ = PieceType.King

    def move(self, move: Move) -> 'Board':
        """
        Applies a move with its all consequences (promotion to a king, etc.)
        :param move: move generated by possible_moves method
        """
        this = self.from_num_repr(self.to_num_repr())
        this._move(move.from_sq, move.to_sq)
        try:
            if move.piece.side == Side.White and move.to_sq.x == 0:
                this._promote(move.to_sq)
            elif move.piece.side == Side.Black and move.to_sq.x == Settings.BoardSize - 1:
                this._promote(move.to_sq)
        except:
            pass

        if isinstance(move, CrownMove):
            for curr_sq, next_sq in zip([move.from_sq] + move.through, move.through):
                for sq in curr_sq.get_squares_to(next_sq)[:-1]:
                    if this.squares[sq]:
                        this._crown(sq)
        self.moves.append(move)

        return this

    def get_possible_simple_moves_from_square(self, square) -> set[SimpleMove]:
        piece = self.squares[square]
        if not piece:
            return set()
        moves = set()

        if piece.type_ == PieceType.Man:
            for target_sq in square.get_forward_neighbours(piece.side):
                if not self.squares[target_sq]:
                    moves.add(SimpleMove(piece, square, target_sq))
        else:
            for direction in (1, 1), (1, -1), (-1, 1), (-1, -1):
                x_step, y_step = direction
                current = square
                while 0 <= current.x <= Settings.BoardSize - 1 and 0 <= current.y <= Settings.BoardSize - 1:
                    current = Square(current.x + x_step, current.y + y_step)
                    if current in self.squares and self.squares[current]:
                        break
                    elif current in self.squares:
                        moves.add(SimpleMove(piece, square, current))

        # Cleanup - remove moves which do not begin with current square.
        moves = {move for move in moves}
        for m in copy.copy(moves):
            if m.from_sq != square:
                moves.remove(m)

        return moves

    def _get_all_moves_from_square(self, square) -> set[SimpleMove]:
        piece = self.squares[square]
        if not piece:
            return set()

        if piece.type_ == PieceType.Man:
            return self.get_possible_simple_moves_from_square(square)
        else:
            moves = set()
            for target_sq in square.diagonal_squares:
                if not self.squares[target_sq]:
                    moves.add(SimpleMove(piece, square, target_sq))
            return moves

    def get_possible_crown_moves_from_square(self, square: Square) -> set[CrownMove]:
        piece = self.squares[square]
        if not piece:
            return set()
        moves = set()

        if piece.type_ == PieceType.Man:
            move_parts_q = [(square, through_sq, target_sq) for through_sq, target_sq in
                            square.neighbours_with_subsequent]
            while move_parts_q:
                from_sq, through_sq, target_sq = move_parts_q.pop()

                if not self.squares.get(through_sq) \
                        or self.squares[through_sq].side == piece.side \
                        or self.squares[target_sq]:
                    continue

                if from_sq == square:
                    moves.add(CrownMove(piece, square, [target_sq]))
                else:
                    for already_started_move in copy.copy(moves):
                        if len(already_started_move.through) > 5:
                            continue
                        if already_started_move.to_sq == from_sq:
                            already_started_move.through.append(target_sq)
                        elif from_sq in already_started_move.through:
                            new_move = already_started_move.get_move_until(from_sq)
                            new_move.through.append(target_sq)
                            moves.add(new_move)

                for subsequent_through_sq, subsequent_target_sq in target_sq.neighbours_with_subsequent:
                    if subsequent_target_sq != from_sq:
                        if not self.squares.get(subsequent_through_sq) \
                                or self.squares[subsequent_through_sq].side == piece.side \
                                or self.squares[subsequent_target_sq]:
                            continue
                        move_parts_q.append((target_sq, subsequent_through_sq, subsequent_target_sq))
        else:
            # If piece is a King
            base_crown_moves: set[SimpleMove] = \
                self._get_all_moves_from_square(square) - self.get_possible_simple_moves_from_square(square)
            base_crown_moves = {move for move in base_crown_moves if not self.squares[move.to_sq]}
            move_parts_q = [(square, move.to_sq) for move in base_crown_moves]
            while move_parts_q:
                if len(move_parts_q) > 100000:
                    move_parts_q = []
                    continue
                from_sq, target_sq = move_parts_q.pop()
                sq_between = from_sq.get_squares_to(target_sq)[:-1]

                # Cannot jump over own pieces
                if any(self.squares[sq] and self.squares[sq].side == piece.side for sq in sq_between):
                    continue

                # Must jump over at least one opposite piece
                if not any(self.squares[sq] and self.squares[sq].side != piece.side for sq in sq_between):
                    continue

                # Must jump to empty sq
                if self.squares[target_sq]:
                    continue

                if from_sq == square:
                    moves.add(CrownMove(piece, square, [target_sq]))
                else:
                    for already_started_move in copy.copy(moves):
                        if already_started_move.to_sq == from_sq:
                            already_started_move.through.append(target_sq)
                        elif from_sq in already_started_move.through:
                            new_move = already_started_move.get_move_until(from_sq)
                            new_move.through.append(target_sq)
                            moves.add(new_move)

                # Generate subsequent moves
                new_board = copy.deepcopy(self)
                new_board._move(square, target_sq)
                for sq in square.get_squares_to(target_sq)[:-1]:
                    if new_board.squares[sq] and new_board.squares[sq].side != piece.side:
                        new_board.squares[sq] = None
                    new_moves: set[SimpleMove] = new_board._get_all_moves_from_square(square) - \
                                                 new_board.get_possible_simple_moves_from_square(square)
                    new_moves = {move for move in new_moves if not new_board.squares[move.to_sq]}
                    for move in new_moves:
                        if move.to_sq != from_sq:
                            move_parts_q.append((move.from_sq, move.to_sq))

        # Cleanup - remove moves which have same crownings (in same or reverse direction) more than once.
        moves = {move for move in moves}
        for crown_move in copy.copy(moves):
            from_sq = crown_move.from_sq
            through = crown_move.through
            sub_moves = list(zip([from_sq] + through, through))
            rev_sub_moves = [(m2, m1) for m1, m2 in sub_moves]

            if len(sub_moves) != len(set(sub_moves)) or any(sub_move in rev_sub_moves for sub_move in sub_moves):
                moves.remove(crown_move)

        # Cleanup - remove moves which do not begin with current square.
        moves = {move for move in moves}
        for crown_move in copy.copy(moves):
            if crown_move.from_sq != square:
                moves.remove(crown_move)

        return moves

    def get_possible_moves_from_square(self, square) -> set[Move]:
        return self.get_possible_simple_moves_from_square(square) | self.get_possible_crown_moves_from_square(square)

    @property
    def possible_moves(self) -> set[Move]:
        moves = set()
        for square in self.squares:
            moves = moves.union(self.get_possible_moves_from_square(square))
        return moves

    def get_possible_moves_of_side(self, side: Side) -> set[Move]:
        moves = set()
        for square, piece in self.squares.items():
            if piece and piece.side == side:
                moves = moves.union(self.get_possible_moves_from_square(square))
        if any(isinstance(move, CrownMove) for move in moves):
            moves = {move for move in moves if isinstance(move, CrownMove)}
            most_steps = max(len(move.through) for move in moves)
            moves = {move for move in moves if len(move.through) == most_steps}
        return moves

    def dump(self, stream=None):
        if stream is None:
            stream = StringIO()
        stream.write('\t' + '\t'.join((str(i + 1) for i in range(Settings.BoardSize))) + '\n')
        for row in range(Settings.BoardSize):
            stream.write(chr(row + 97) + '\t')
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
            stream.write(chr(row + 97) + '\t\n')
        stream.write('\t' + '\t'.join((str(i + 1) for i in range(Settings.BoardSize))) + '\n')

    def __hash__(self):
        return hash(self.to_num_repr())
