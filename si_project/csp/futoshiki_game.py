import itertools
from typing import Iterable, Callable

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

    @property
    def checks(self) -> Iterable[Callable]:
        return (
            self._check_row_elems_uniqueness,
            self._check_horizontal_constraints,
            self._check_vertical_constraints,
            self._check_col_elems_uniqueness
        )

    def _check_row_elems_uniqueness(self, matrix) -> bool:
        for i in range(len(matrix)):
            elems = [el for el in matrix[i] if el is not None]
            if len(elems) != len(set(elems)):
                return False
        return True

    def _check_col_elems_uniqueness(self, matrix) -> bool:
        return self._check_row_elems_uniqueness(list(zip(*matrix)))

    def _check_vertical_constraints(self, matrix):
        for i in range(self.size - 1):
            for j in range(self.size):
                if None not in (self.vertical_constraints[i][j],
                                matrix[i][j], matrix[i + 1][j]):
                    if self.vertical_constraints[i][j] == '>':
                        if matrix[i][j] <= matrix[i + 1][j]:
                            return False
                    else:
                        if matrix[i][j] >= matrix[i + 1][j]:
                            return False
        return True

    def _check_horizontal_constraints(self, matrix):
        for i in range(self.size):
            for j in range(self.size - 1):
                if None not in (self.horizontal_constraints[i][j],
                                matrix[i][j], matrix[i][j + 1]):
                    if self.horizontal_constraints[i][j] == '>':
                        if matrix[i][j] <= matrix[i][j + 1]:
                            return False
                    else:
                        if matrix[i][j] >= matrix[i][j + 1]:
                            return False
        return True

    def print_matrix(self, matrix=None):
        if not matrix:
            matrix = self.matrix
        for i in range(self.size):
            # Print row, without last elem but with following constr.
            line = zip([num if num is not None else 'x' for num in matrix[i]], [ch if ch is not None else '-' for ch in self.horizontal_constraints[i]])
            line = list(itertools.chain(*line)) + [(matrix[i][-1] if matrix[i][-1] is not None else 'x')]
            print(*line)
            # Print vertical constraints.
            if i != self.size - 1:
                print(*[ch if ch is not None else '-' for ch
                        in self.vertical_constraints[i]], sep='   ')
