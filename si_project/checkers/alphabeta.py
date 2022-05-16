from si_project.checkers.models import Side, Board


def alphabeta(side: Side, board: Board, alpha: int, beta: int, depth=0) -> int:
    """
    Returns best possible score for a given side from current board.
    """
    if abs(board.rating) == 100 or depth >= 3:
        return board.rating
    next_boards = (board.move(move) for move in board.get_possible_moves_of_side(side))
    if side == Side.White:
        for next_board in next_boards:
            score = alphabeta(side.next, next_board, alpha, beta, depth + 1)
            if score > alpha:
                alpha = score
            if alpha >= beta:
                return alpha
        return alpha
    else:
        for next_board in next_boards:
            score = alphabeta(side.next, next_board, alpha, beta, depth + 1)
            if score < beta:
                beta = score
            if alpha >= beta:
                return beta
        return beta
