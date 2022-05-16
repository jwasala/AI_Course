import sys

from si_project.checkers.models import Board, Side

b = Board.populate_initial_board()

current_side = Side.Black

print('Game started')

while True:
    if b.rating == 100:
        print('Whites Won')
        break
    elif b.rating == -100:
        print('Blacks Won')
    print(f'{b.rating=}')

    b.dump(sys.stdout)

    possible_moves = sorted(list(b.get_possible_moves_of_side(current_side)), key=lambda m: m.__str__())

    print(f'Current side: {current_side}')
    print('Possible moves: \n\t--> ', end='')
    print('\n\t--> '.join(f'{move} ({i})' for i, move in enumerate(possible_moves)))
    while True:
        try:
            move = possible_moves[int(input('Type move number: '))]
            break
        except:
            pass
    b.move(move)

    current_side = current_side.next
