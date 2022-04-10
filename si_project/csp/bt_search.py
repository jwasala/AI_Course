from typing import Generic

from .problem import Problem, VLabel, VValue


class BTSearch(Generic[VLabel, VValue]):
    _solutions_count = 0
    _steps_count = 0
    _solutions = set()

    @classmethod
    def _bt_search(cls,
                   assigned_vars: dict[VLabel, VValue],
                   unassigned_vars: list[VLabel],
                   domain: dict[VLabel, list[VValue]],
                   problem: Problem):
        if not unassigned_vars:
            return tuple(assigned_vars)
        var, unassigned_vars = unassigned_vars[0], unassigned_vars[1:]
        for val in domain[var]:
            cls._steps_count += 1
            if cls._steps_count % 100000 == 0:
                print(f'Steps: {cls._steps_count}')
            if problem.check_constraints((var, val), assigned_vars):
                assigned_vars[var] = val
                result = cls._bt_search(assigned_vars, unassigned_vars, domain, problem)
                if result and result not in cls._solutions:
                    cls._solutions.add(result)
                    cls._solutions_count += 1
                    print(f'Solution {cls._solutions_count} found'
                          f' (after {cls._steps_count} steps):')
                    problem.print_with_assigned_variables(assigned_vars)
                del assigned_vars[var]
        return None

    @classmethod
    def bt_search(cls,
                  problem: Problem):
        cls._solutions_count = 0
        cls._steps_count = 0
        cls._bt_search({}, problem.variables, problem.domains, problem)
