from si_project.checkers.models import Side, PieceType


def base_rating(board) -> int:
    is_any_white = False
    is_any_black = False
    total_sum = 0

    for sq, piece in board.squares.items():
        if piece:
            piece_value = sq.sector_multiplier * (3 if piece.type_ == PieceType.King else 1)
            if piece.side == Side.White:
                is_any_white = True
            else:
                is_any_black = True
                piece_value *= -1
            total_sum += piece_value

    if is_any_black and not is_any_white:
        return -1000
    elif is_any_white and not is_any_black:
        return 1000
    else:
        return total_sum


def no_king_multip_rating(board) -> int:
    is_any_white = False
    is_any_black = False
    total_sum = 0

    for sq, piece in board.squares.items():
        if piece:
            piece_value = sq.sector_multiplier
            if piece.side == Side.White:
                is_any_white = True
            else:
                is_any_black = True
                piece_value *= -1
            total_sum += piece_value

    if is_any_black and not is_any_white:
        return -1000
    elif is_any_white and not is_any_black:
        return 1000
    else:
        return total_sum


def forward_extra_rating(board) -> int:
    is_any_white = False
    is_any_black = False
    total_sum = 0

    for sq, piece in board.squares.items():
        if piece:
            piece_value = sq.sector_multiplier * (3 if piece.type_ == PieceType.King else 1)
            if piece.side == Side.White:
                is_any_white = True
                if sq.x < 4:
                    piece_value *= 3
            else:
                is_any_black = True
                if sq.x >= 4:
                    piece_value *= 3
                piece_value *= -1
            total_sum += piece_value

    if is_any_black and not is_any_white:
        return -1000
    elif is_any_white and not is_any_black:
        return 1000
    else:
        return total_sum
