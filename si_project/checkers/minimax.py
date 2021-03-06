from si_project.checkers.models import Side, Board


def minimax(side: Side, board: Board, depth=4, rating_heuristic=None) -> int:
    """
    Returns best possible score for a given side from current board.
    """
    if abs(rating_heuristic(board)) == 1000 or depth == 0:
        return rating_heuristic(board)
    next_boards = (board.move(move) for move in board.get_possible_moves_of_side(side))
    if not next_boards:
        return rating_heuristic(board)
    if side == Side.White:
        res = [minimax(Side.Black, board, depth - 1, rating_heuristic) for board in next_boards]
        if not res:
            return rating_heuristic(board)
        return max(res)
    else:
        res = [minimax(Side.White, board, depth - 1, rating_heuristic) for board in next_boards]
        if not res:
            return rating_heuristic(board)
        return min(res)
