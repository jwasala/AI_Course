from .problem import Problem, Variable


# Not thread safe :(
_solutions_count = 0
_steps_count = 0
_solutions = set()


def _bt_search(assigned_vars: list[Variable], unassigned_vars: list[Variable],
               problem: Problem):
    global _solutions_count
    global _steps_count
    if not unassigned_vars:
        return tuple(assigned_vars)
    var, unassigned_vars = unassigned_vars[0], unassigned_vars[1:]
    for val in problem.domain:
        if problem.is_consistent(assigned_vars, var[0], val):
            var = (var[0], val)
            assigned_vars.append(var)
            _steps_count += 1
            result = _bt_search(assigned_vars, unassigned_vars, problem)
            if result and result not in _solutions:
                _solutions.add(result)
                _solutions_count += 1
                print(f'Solution {_solutions_count} found'
                      f' (after {_steps_count} steps):')
                problem.print_merged_matrix(result)
            assigned_vars.pop()
    return None


def bt_search(problem: Problem):
    global _solutions_count
    global _steps_count
    _solutions_count = 0
    _steps_count = 0
    a = []
    u = problem.generate_unassigned_vars()
    _bt_search(a, u, problem)
