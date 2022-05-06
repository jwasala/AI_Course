from copy import deepcopy
from functools import cached_property
from itertools import product, combinations, chain
from operator import ne, gt, lt
from typing import Callable

from .problem import Problem


class FutoshikiGame(Problem):
    Variable = [tuple[int, int], int]

    def __init__(self, size: int):
        self.size = size
        self.domain = list(range(1, size + 1))
        self.matrix = \
            [[None for _ in range(size)] for _ in range(size)]
        self.vertical_constraints: list[list[str | None]] = \
            [[None for _ in range(size)] for _ in range(size - 1)]
        self.horizontal_constraints: list[list[str | None]] = \
            [[None for _ in range(size - 1)] for _ in range(size)]

    @cached_property
    def variables(self) -> list[tuple[int, int]]:
        return list(product(range(self.size), repeat=2))

    @cached_property
    def domains(self) -> dict[tuple[int, int], list[int]]:
        base_domain = list(range(1, self.size + 1))
        return {(i, j): base_domain if self.matrix[i][j] is None else [self.matrix[i][j]] for i, j in self.variables}

    @cached_property
    def constraints(self) -> dict[tuple[tuple[int, int], tuple[int, int]], set[Callable[[Variable, Variable], bool]]]:
        c = {pair: set() for pair in product(self.variables, repeat=2)}

        def values_ne(v1, v2):
            return v1[1] != v2[1]

        def values_lt(v1, v2):
            return v1[1] < v2[1]

        def values_gt(v1, v2):
            return v1[1] > v2[1]

        # Row and col internal uniqueness
        for i in range(self.size):
            for j1, j2 in product(range(self.size), repeat=2):
                if j1 != j2:
                    c[((i, j1), (i, j2))].add(values_ne)
                    c[((i, j2), (i, j1))].add(values_ne)
                    c[((j1, i), (j2, i))].add(values_ne)
                    c[((j2, i), (j1, i))].add(values_ne)

        # Horizontal constraints
        for i, row in enumerate(self.horizontal_constraints):
            for j, constr in enumerate(row):
                if constr is not None:
                    c[((i, j), (i, j + 1))].add(values_gt if constr == '>' else values_lt)
                    c[((i, j + 1), (i, j))].add(values_lt if constr == '>' else values_gt)

        # Vertical constraints
        for i, row in enumerate(self.vertical_constraints):
            for j, constr in enumerate(row):
                if constr is not None:
                    c[((i, j), (i + 1, j))].add(values_gt if constr == '>' else values_lt)
                    c[((i + 1, j), (i, j))].add(values_lt if constr == '>' else values_gt)
        return c

    def print_with_assigned_variables(self, assigned_variables: dict[tuple[int, int], int]):
        matrix = deepcopy(self.matrix)
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) in assigned_variables:
                    matrix[i][j] = assigned_variables[(i, j)]
        for i in range(self.size):
            # Print row, without last elem but with following constr.
            line = zip([num if num is not None else 'x' for num in matrix[i]], [ch if ch is not None else '-' for ch in self.horizontal_constraints[i]])
            line = list(chain(*line)) + [(matrix[i][-1] if matrix[i][-1] is not None else 'x')]
            print(*line)
            # Print vertical constraints.
            if i != self.size - 1:
                print(*[ch if ch is not None else '-' for ch
                        in self.vertical_constraints[i]], sep='   ')
