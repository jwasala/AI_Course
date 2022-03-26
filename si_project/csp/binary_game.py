from .problem import Problem, Variable


class BinaryGame(Problem):
    def __init__(self, size: int):
        if size % 2 != 0:
            raise ValueError
        self.matrix: list[list[int | None]] = \
            [[None for _ in range(size)] for _ in range(size)]
        self.domain: list[int] = [0, 1]
        self.size: int = size

    def print_matrix(self, matrix=None):
        if not matrix:
            matrix = self.matrix
        for row in matrix:
            print(*[cell if cell is not None else 'x' for cell in row])

    def is_consistent(self, assigned_vars: list[Variable],
                      next_var: tuple[int, int], next_val: int) -> bool:
        mtx = self.merge_matrix(assigned_vars, next_var, next_val)
        checks = (
            self._check_row_symmetry,
            self._check_col_symmetry,
            self._check_row_triples,
            self._check_col_triples,
            self._check_row_uniqueness,
            self._check_col_uniqueness
        )
        for check in checks:
            if not check(mtx):
                return False
        return True

    def _check_domain(self, matrix) -> bool:
        for row in matrix:
            for cell in row:
                if cell not in (*self.domain, None):
                    return False
        return True

    def _check_row_uniqueness(self, matrix) -> bool:
        rows = [str(row) for row in matrix if None not in row]
        return len(rows) == len(set(rows))

    def _check_col_uniqueness(self, matrix) -> bool:
        return self._check_row_uniqueness([*zip(*matrix)])

    def _check_row_symmetry(self, matrix) -> bool:
        rows = [row for row in matrix if None not in row]
        for row in rows:
            if sum(row) != self.size / 2:
                return False
        return True

    def _check_col_symmetry(self, matrix) -> bool:
        return self._check_row_symmetry([*zip(*matrix)])

    def _check_row_triples(self, matrix) -> bool:
        if self.size < 3:
            return True
        for row in matrix:
            for i in range(self.size - 2):
                if row[i] == row[i + 1] == row[i + 2] and row[i] is not None:
                    return False
        return True

    def _check_col_triples(self, matrix) -> bool:
        return self._check_row_triples([*zip(*matrix)])
