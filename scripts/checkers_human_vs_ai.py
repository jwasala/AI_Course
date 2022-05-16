import asyncio
import sys

from si_project.checkers.models import Board, Side
from si_project.checkers.minimax import minimax

# kartkówka:
# przykładowe drzewo gry - co w jakiej sytuacji zrobi algorytm
# minimax, alfa-beta


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
            possible_moves = sorted(list(b.get_possible_moves_of_side(current_side)), key=lambda m: m.__str__())
            print('Dostępne ruchy: \n\t--> ', end='')
            print('\n\t--> '.join(f'{move} ({i})' for i, move in enumerate(possible_moves)))
            while True:
                try:
                    move = possible_moves[int(input('Podaj numer ruchu: '))]
                    break
                except:
                    pass
            b = b.move(move)

        current_side = current_side.next


if __name__ == '__main__':
    asyncio.run(main())
