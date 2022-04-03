from typing import Callable

from .problem import Problem, Variable

# Not thread safe :(
_solutions_count = 0
_steps_count = 0
_solutions = set()


def _bt_search(assigned_vars: list[Variable], unassigned_vars: list[Variable], domain: dict[Variable, list[int]],
               problem: Problem):
    global _solutions_count
    global _steps_count
    if not unassigned_vars:
        return tuple(assigned_vars)
    var, unassigned_vars = unassigned_vars[0], unassigned_vars[1:]
    for val in domain[var[0]]:
        _steps_count += 1
        if _steps_count % 100000 == 0:
            print(f'Steps: {_steps_count}')
        if problem.is_consistent(assigned_vars, var[0], val):
            var = (var[0], val)
            assigned_vars.append(var)
            result = _bt_search(assigned_vars, unassigned_vars, domain, problem)
            if result and result not in _solutions:
                _solutions.add(result)
                _solutions_count += 1
                print(f'Solution {_solutions_count} found'
                      f' (after {_steps_count} steps):')
                problem.print_merged_matrix(result)
            assigned_vars.pop()
    return None


def bt_search(problem: Problem, sort_variables: Callable[[list[Variable]], list[Variable]] = lambda x: x):
    global _solutions_count
    global _steps_count
    _solutions_count = 0
    _steps_count = 0
    a = []
    u = problem.generate_unassigned_vars()
    u = sort_variables(u)
    _bt_search(a, u, {var: problem.domain for var in u}, problem)
