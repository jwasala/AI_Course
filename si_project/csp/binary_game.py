from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from itertools import product, combinations
from operator import ne
from typing import Callable

from .problem import Problem


class BGVLabelType(Enum):
    Row = 1
    Col = 2


@dataclass
class BGVLabel:
    type: BGVLabelType
    index: int

    def __hash__(self):
        return hash(f'{self.type}.{self.index}')


class BinaryGame(Problem[BGVLabel, list[int]]):
    Variable = tuple[BGVLabel, list[int]]

    def __init__(self, size: int):
        if size % 2 != 0:
            raise ValueError
        self.matrix: list[list[int | None]] = [[None for _ in range(size)] for _ in range(size)]
        self.size: int = size

    @cached_property
    def variables(self) -> list[BGVLabel]:
        return [BGVLabel(var_type, index) for var_type, index in product(BGVLabelType, range(self.size))]

    @cached_property
    def domains(self) -> dict[BGVLabel, list[list[int]]]:
        domains = {}
        # base_dom is a superset of every variable's domain
        base_dom = list(product([0, 1], repeat=self.size))
        # Filter out values where number of zeroes and ones is not equal
        base_dom = [val for val in base_dom if sum(val) == self.size // 2]
        # Filter out values where there are
        base_dom = [val for val in base_dom if all(
            window_sum not in [0, 3] for window_sum in (sum(window) for window in zip(val, val[1:], val[2:]))
        )]
        for variable in self.variables:
            domains[variable] = deepcopy(base_dom)
            # Filter out values which do not comply with pre-defined cells in the game matrix
            if variable.type == BGVLabelType.Col:
                for i, mtx_val in enumerate([self.matrix[i][variable.index] for i in range(self.size)]):
                    if mtx_val is not None:
                        domains[variable] = [dom_val for dom_val in domains[variable] if dom_val[i] == mtx_val]
            else:
                for j, mtx_val in enumerate(self.matrix[variable.index]):
                    if mtx_val is not None:
                        domains[variable] = [dom_val for dom_val in domains[variable] if dom_val[j] == mtx_val]
        return domains

    @cached_property
    def constraints(self) -> dict[tuple[BGVLabel, BGVLabel], set[Callable[[Variable, Variable], bool]]]:
        def is_row_and_col_intersection_consistent(row: BinaryGame.Variable, col: BinaryGame.Variable) -> bool:
            row_label, row_value = row
            col_label, col_value = col
            return row_value[col_label.index] == col_value[row_label.index]

        constraints = {(var_1, var_2): set() for var_1, var_2 in product(self.variables, repeat=2)}

        # Add uniqueness constraints for every pair of rows and every pair of cols
        for var_type in BGVLabelType:
            for var_1, var_2 in combinations((var for var in self.variables if var.type == var_type), r=2):
                constraints[(var_1, var_2)].add(ne)
                constraints[(var_2, var_1)].add(ne)

        # Add cell consistency constraints for every pair of row and col
        for row in (var for var in self.variables if var.type == BGVLabelType.Row):
            for col in (var for var in self.variables if var.type == BGVLabelType.Col):
                constraints[(row, col)].add(is_row_and_col_intersection_consistent)
                constraints[(col, row)].add(is_row_and_col_intersection_consistent)

        return constraints

    def print_with_assigned_variables(self, assigned_variables: dict[BGVLabel, list[int]]):
        for i in range(self.size):
            if BGVLabel(BGVLabelType.Row, i) in assigned_variables:
                print(*assigned_variables[BGVLabel(BGVLabelType.Row, i)])
            else:
                print(*self.matrix[i])
