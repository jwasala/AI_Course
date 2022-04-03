from dataclasses import dataclass
from itertools import combinations
from operator import lt, gt, ne
from typing import Callable

from si_project.csp import FutoshikiGame
from si_project.csp.bt_fc_search import _bt_fc_search
from si_project.csp.bt_search import _bt_search


@dataclass
class Variable:
    label: tuple[int, int] | str
    current_value: int | None
    domain: list[int]

    def __ne__(self, other: 'Variable'):
        return self.current_value.__ne__(other.current_value)

    def __lt__(self, other: 'Variable'):
        return self.current_value.__lt__(other.current_value)

    def __gt__(self, other: 'Variable'):
        return self.current_value.__gt__(other.current_value)

    def with_val(self, val):
        return Variable(self.label, val, self.domain)


@dataclass
class Constraint:
    var1: Variable
    var2: Variable
    constraint: Callable[[Variable, Variable], bool]


@dataclass
class ConstraintGraph:
    variables: list[Variable]
    constraints: list[Constraint]


def futoshiki_problem_to_constraint_graph(fg: FutoshikiGame):
    variables: dict[tuple[int, int], Variable] = {}
    for i, row in enumerate(fg.matrix):
        for j, cell in enumerate(row):
            if cell is None:
                variables[(i, j)] = Variable((i, j), None, fg.domain)
            else:
                variables[(i, j)] = Variable((i, j), cell, [cell])
    constraints: list[Constraint] = []
    # Adding inequality binary constraints.
    # Vertical constraints
    for i in range(fg.size - 1):
        for j in range(fg.size):
            if fg.vertical_constraints[i][j]:
                if fg.vertical_constraints[i][j] == '>':
                    func = gt
                else:
                    func = lt
                constraints.append(Constraint(variables[(i, j)], variables[(i + 1, j)], func))
    # Horizontal constraints
    for i in range(fg.size):
        for j in range(fg.size - 1):
            if fg.horizontal_constraints[i][j]:
                if fg.horizontal_constraints[i][j] == '>':
                    func = gt
                else:
                    func = lt
                constraints.append(Constraint(variables[(i, j)], variables[(i, j + 1)], func))
    # Adding constraints for row uniqueness.
    for i in range(fg.size):
        for var1, var2 in combinations((var for coord, var in variables.items() if coord[0] == i), r=2):
            constraints.append(Constraint(var1, var2, ne))
    # Adding constraints for col uniqueness.
    for j in range(fg.size):
        for var1, var2 in combinations((var for coord, var in variables.items() if coord[1] == j), r=2):
            constraints.append(Constraint(var1, var2, ne))
    return ConstraintGraph(list(variables.values()), constraints)


def variables_to_futoshiki_variables(variables: list[Variable]) -> tuple[
    list[tuple[tuple[int, int], int | None]], list[tuple[tuple[int, int], int | None, list[int]]]]:
    fg_vars = []
    fg_vars_with_domain = []
    for var in variables:
        fg_vars.append((var.label, None))
        fg_vars_with_domain.append((var.label, None, var.domain))
    return fg_vars, fg_vars_with_domain


def _remove_inconsistent_values(x: Variable, y: Variable, constraint: Callable[[Variable, Variable], bool]):
    org_len = len(x.domain)
    x.domain = [val_x for val_x in x.domain if
                any(constraint(x.with_val(val_x), y.with_val(val_y)) for val_y in y.domain)]
    return len(x.domain) != org_len


def ac(cg: ConstraintGraph, fg: FutoshikiGame):
    q = cg.constraints
    while q:
        arc, q = q[0], q[1:]
        if _remove_inconsistent_values(arc.var1, arc.var2, arc.constraint):
            for arc2 in cg.constraints:
                if arc2.var1 != arc.var2 and arc2.var2 == arc.var1 and arc2 not in q:
                    q.append(arc2)

    uv, uv_with_dom = variables_to_futoshiki_variables(cg.variables)
    _bt_search([], uv, {v[0]: v[2] for v in uv_with_dom}, fg)
