import builtins
import sys
import traceback
from datetime import datetime
from itertools import combinations

from si_project.checkers.models import Board, Side
from si_project.checkers.alphabeta import alphabeta
from si_project.checkers.minimax import minimax
from si_project.checkers.ratings import base_rating, forward_extra_rating, no_king_multip_rating

f = open('output_checkers.txt', mode='w')

def print(s):
    builtins.print(s)
    f.write(s + '\n')


def main():
    print(','.join([
        'Nr gry',
        'Nr ruchu',
        'Akcja',
        'Rating',
        'Czas od poczatku gry [ms]',
        'Rating',
        'Algorytm',
        'Max glebokosc'
    ]))
    # print('Początek gry')
    game_i = 0

    for depth in (3, 5, 10, 15, 25, 35):
        for algorithm in (alphabeta, minimax):
            if algorithm == minimax and depth != 3:
                continue
            for rating_white, rating_black in combinations((base_rating, forward_extra_rating, no_king_multip_rating), r=2):
                games_left = 5
                while games_left > 0:
                    start = datetime.now()
                    b = Board.populate_initial_board()
                    current_side = Side.White
                    games_left -= 1
                    game_i += 1
                    moves_count = 0
                    try:
                        while True:
                            if b.rating == 1000:
                                state = 'Biale wygraly'
                            elif b.rating == -1000:
                                state = 'Czarne wygraly'
                            else:
                                state = None
                            if state:
                                print(','.join([
                                    str(game_i),
                                    str(moves_count),
                                    state,
                                    f'{rating_white.__name__} / {rating_black.__name__}',
                                    str((datetime.now() - start).total_seconds() * 1000),
                                    str(b.rating),
                                    algorithm.__name__,
                                    str(depth)
                                ]))
                                break
                            if current_side == Side.Black:
                                moves = list(b.get_possible_moves_of_side(Side.Black))
                                if not moves:
                                    break
                                values = [algorithm(Side.White, b.move(move), depth, rating_black) for move in moves]
                                best_move = moves[values.index(min(values))]
                                b = b.move(best_move)
                                print(','.join([
                                    str(game_i),
                                    str(moves_count),
                                    'Ruch czarnych',
                                    rating_black.__name__,
                                    str((datetime.now() - start).total_seconds() * 1000),
                                    str(b.rating),
                                    algorithm.__name__,
                                    str(depth)
                                ]))
                            else:
                                moves = list(b.get_possible_moves_of_side(Side.White))
                                if not moves:
                                    break
                                values = [algorithm(Side.Black, b.move(move), depth, rating_white) for move in moves]
                                best_move = moves[values.index(max(values))]
                                b = b.move(best_move)
                                print(','.join([
                                    str(game_i),
                                    str(moves_count),
                                    'Ruch białych',
                                    rating_white.__name__,
                                    str((datetime.now() - start).total_seconds() * 1000),
                                    str(b.rating),
                                    algorithm.__name__,
                                    str(depth)
                                ]))
                            moves_count += 1
                            current_side = current_side.next
                    except:
                        pass


if __name__ == '__main__':
    try:
        main()
    except:
        f.close()
