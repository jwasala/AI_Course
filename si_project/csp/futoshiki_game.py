import itertools
from typing import Iterable

from .problem import Problem, Variable


class FutoshikiGame(Problem):
    def __init__(self, size: int):
        self.size = size
        self.domain = list(range(1, size + 1))
        self.matrix = \
            [[None for _ in range(size)] for _ in range(size)]
        self.vertical_constraints: list[list[str | None]] = \
            [[None for _ in range(size)] for _ in range(size - 1)]
        self.horizontal_constraints: list[list[str | None]] = \
            [[None for _ in range(size - 1)] for _ in range(size)]

    def is_consistent(self, assigned_vars: list[Variable],
                      next_coord: tuple[int, int], next_val: int):
        pass

    def print_matrix(self, matrix=None):
        if not matrix:
            matrix = self.matrix
        for i in range(self.size):
            # Print row, without last elem but with following constr.
            line = zip([num if num is not None else 'x' for num in self.matrix[i]], [ch if ch is not None else '-' for ch in self.horizontal_constraints[i]])
            line = list(itertools.chain(*line)) + [(self.matrix[i][-1] if self.matrix[i][-1] is not None else 'x')]
            print(*line)
            # Print vertical constraints.
            if i != self.size - 1:
                print(*[ch if ch is not None else '-' for ch
                        in self.vertical_constraints[i]], sep='   ')
