from si_project.checkers.models import Side, Board


def alphabeta(side: Side, board: Board, depth: int = 4, rating_heuristic=None, alpha: int = 1000,
              beta: int = -1000) -> int:
    """
    Returns best possible score for a given side from current board.
    """
    if abs(rating_heuristic(board)) == 1000 or depth == 0:
        return rating_heuristic(board)
    next_boards = (board.move(move) for move in board.get_possible_moves_of_side(side))
    if side == Side.White:
        for next_board in next_boards:
            score = alphabeta(side.next, next_board, depth - 1, rating_heuristic, alpha, beta)
            if score > alpha:
                alpha = score
            if alpha >= beta:
                return alpha
        return alpha
    else:
        for next_board in next_boards:
            score = alphabeta(side.next, next_board, depth - 1, rating_heuristic, alpha, beta)
            if score < beta:
                beta = score
            if alpha >= beta:
                return beta
        return beta
