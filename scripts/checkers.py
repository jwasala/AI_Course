import sys

from si_project.checkers.models import Board


b = Board.populate_initial_board()

b.dump(sys.stdout)
