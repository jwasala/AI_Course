import sys

from si_project.checkers.models import Board


b = Board.populate_initial_board(8)

b.dump(sys.stdout)
