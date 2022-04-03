from copy import deepcopy

from .problem import Problem, Variable

_solutions_count = 0
_steps_count = 0
_solutions = set()


def are_neighbors(var1: Variable, var2: Variable) -> bool:
    return abs(var1[0][0] - var2[0][0]) + abs(var1[0][1] - var2[0][1]) == 1


def _bt_fc_search(assigned_vars: list[Variable],
                  unassigned_vars: list[Variable],
                  curr_domain: dict[tuple[int, int], list[int]],
                  problem: Problem):
    global _solutions_count
    global _steps_count
    if not unassigned_vars:
        return tuple(assigned_vars)
    var, unassigned_vars = unassigned_vars[0], unassigned_vars[1:]
    for val in curr_domain[var[0]]:
        _steps_count += 1
        if _steps_count % 100000 == 0:
            print(f'Steps: {_steps_count}')
        if problem.is_consistent(assigned_vars, var[0], val):
            var = (var[0], val)
            assigned_vars.append(var)
            curr_domain_copy = deepcopy(curr_domain)
            neighbors = [v for v in unassigned_vars if are_neighbors(v, var)]
            for var_y in neighbors:
                curr_domain_copy[var_y] = [x for x in curr_domain_copy[var_y[0]] if
                                         problem.is_consistent(assigned_vars, var_y[0], x)]
            if all(curr_domain_copy[var_y[0]] for var_y in neighbors):
                result = _bt_fc_search(assigned_vars, unassigned_vars, curr_domain_copy, problem)
                if result and result not in _solutions:
                    _solutions.add(result)
                    _solutions_count += 1
                    print(f'Solution {_solutions_count} found'
                          f' (after {_steps_count} steps):')
                    problem.print_merged_matrix(result)
            assigned_vars.pop()
    return None


def bt_fc_search(problem: Problem):
    global _solutions_count
    global _steps_count
    _solutions_count = 0
    _steps_count = 0
    a = []
    u = problem.generate_unassigned_vars()
    d = {v: deepcopy(problem.domain) for v in u}
    _bt_fc_search(a, u, d, problem)
