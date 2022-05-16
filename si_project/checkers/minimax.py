import asyncio

from si_project.checkers.models import Side, Board


async def minimax(side: Side, board: Board, depth=0) -> int:
    """
    Returns best possible score for a given side from current board.
    """
    if abs(board.rating) == 100 or depth >= 3:
        return board.rating
    next_boards = (board.move(move) for move in board.get_possible_moves_of_side(side))
    if side == Side.White:
        child_vals = await asyncio.gather(*[minimax(Side.Black, board, depth + 1) for board in next_boards])
        return max(child_vals)
    else:
        child_vals = await asyncio.gather(*[minimax(Side.White, board, depth + 1) for board in next_boards])
        return min(child_vals)
