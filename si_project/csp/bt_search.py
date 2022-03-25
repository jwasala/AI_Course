from .problem import Problem, Variable


def _bt_search(assigned_vars: list[Variable], unassigned_vars: list[Variable],
               problem: Problem):
    if not unassigned_vars:
        return tuple(assigned_vars)
    var, unassigned_vars = unassigned_vars[0], unassigned_vars[1:]
    for val in problem.domain:
        if problem.is_consistent(assigned_vars, var[0], val):
            var = (var[0], val)
            assigned_vars.append(var)
            result = _bt_search(assigned_vars, unassigned_vars, problem)
            if result:
                return result
            assigned_vars.pop()
    return None


def bt_search(problem: Problem):
    a = []
    u = problem.generate_unassigned_vars()
    result = _bt_search(a, u, problem)
    problem.print_merged_matrix(result)
