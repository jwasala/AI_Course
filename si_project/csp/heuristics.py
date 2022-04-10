from collections import Counter

from si_project.csp import BinaryGame
from si_project.csp.problem import Problem


def order_variables_by_domain_size(problem: Problem):
    return list(sorted(problem.variables, key=lambda var: len(problem.domains[var])))


def binary_order_variables_by_same_index(problem: BinaryGame):
    return list(sorted(problem.variables, key=lambda var: var.index))


def order_variables_by_most_constraints(problem: Problem):
    c = problem.constraints.items()
    counts = Counter({v1: len(c) for (v1, _), c in c}) + Counter({v2: len(c) for (_, v2), c in c})
    return list(sorted(problem.variables, key=lambda var: counts[var]))
