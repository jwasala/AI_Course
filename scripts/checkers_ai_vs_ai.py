import asyncio
import functools
import sys

from si_project.checkers.models import Board, Side
from si_project.checkers.minimax import minimax


async def main():
    b = Board.populate_initial_board()
    current_side = Side.White
    print('Początek gry')

    while True:
        if b.rating == 100:
            print('Białe zwyciężyły!')
            break
        elif b.rating == -100:
            print('Czarne zwyciężyły!')
            break

        b.dump(sys.stdout)

        if b.rating > 0:
            print(f'Przewaga białych - {b.rating} pkt')
        elif b.rating < 0:
            print(f'Przewaga czarnych - {abs(b.rating)} pkt')
        else:
            print(f'Brak przewagi żadnej ze stron')

        if current_side == Side.White:
            print('Ruch białych')
        else:
            print('Ruch czarnych')
        if current_side == Side.Black:
            moves = list(b.get_possible_moves_of_side(Side.Black))
            values = await asyncio.gather(*[minimax(Side.White, b.move(move)) for move in moves])
            best_move = moves[values.index(min(values))]
            b = b.move(best_move)
            print(f'Ruch czarnych: {best_move}')
        else:
            moves = list(b.get_possible_moves_of_side(Side.White))
            values = await asyncio.gather(*[minimax(Side.Black, b.move(move)) for move in moves])
            best_move = moves[values.index(max(values))]
            b = b.move(best_move)
            print(f'Ruch białych: {best_move}')

        current_side = current_side.next


if __name__ == '__main__':
    asyncio.run(main())
