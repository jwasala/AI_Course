import copy
from typing import Iterable, Callable

Variable = tuple[tuple[int, int], int | None]


class Problem:
    domain: list[int]
    matrix: list[list[int | None]]

    @property
    def checks(self) -> Iterable[Callable]:
        pass

    def is_consistent(self, assigned_vars: list[Variable],
                      next_coord: tuple[int, int], next_val: int):
        mtx = self.merge_matrix(assigned_vars, next_coord, next_val)
        for check in self.checks:
            if not check(mtx):
                return False
        return True

    def print_matrix(self, matrix=None):
        pass

    def print_merged_matrix(self, assigned_vars: Iterable[Variable]):
        merged = self._merge_matrix(assigned_vars)
        return self.print_matrix(merged)

    def generate_unassigned_vars(self):
        u: list[Variable] = []
        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                if cell is None:
                    u.append(((i, j), None))
        return u

    def _merge_matrix(self, assigned_vars: Iterable[Variable]):
        mtx = copy.deepcopy(self.matrix)
        for (i, j), val in assigned_vars:
            mtx[i][j] = val
        return mtx

    def merge_matrix(self, assigned_vars: Iterable[Variable],
                     next_var: tuple[int, int], next_val: int):
        return self._merge_matrix([*assigned_vars, (next_var, next_val)])

