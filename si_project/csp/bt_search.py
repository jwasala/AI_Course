from .problem import Problem


def _bt_search(a, u, problem: Problem):
    if not u:
        return tuple(a)
    var, u = u[0], u[1:]
    for val in problem.domain:
        if problem.is_consistent(a, var[0], val):
            var = (var[0], val)
            a.append(var)
            result = _bt_search(a, u, problem)
            if result:
                return result
            a.pop()
    return None


def bt_search(problem: Problem):
    a = []
    u = problem.generate_unassigned_vars()
    result = _bt_search(a, u, problem)
    problem.print_merged_matrix(result)
