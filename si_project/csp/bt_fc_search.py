from copy import deepcopy
from typing import Generic

from .problem import Problem, VLabel, VValue


class BTFCSearch(Generic[VLabel, VValue]):
    _solutions_count = 0
    _steps_count = 0
    _solutions = set()

    @classmethod
    def _bt_fc_search(cls,
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
                domain_cp = deepcopy(domain)
                neighbors = (var_y for var_y in unassigned_vars if problem.constraints[(var_y, var)])
                for var_y in unassigned_vars:
                    if problem.constraints[(var_y, var)] or problem.constraints[(var, var_y)]:
                        domain_cp[var_y] = [val_y for val_y in domain_cp[var_y] if
                                            problem.check_constraints((var_y, val_y), assigned_vars)]
                if all(domain_cp[var_y] for var_y in neighbors):
                    result = cls._bt_fc_search(assigned_vars, unassigned_vars, domain_cp, problem)
                    if result and result not in cls._solutions:
                        cls._solutions.add(result)
                        cls._solutions_count += 1
                        print(f'Solution {cls._solutions_count} found'
                              f' (after {cls._steps_count} steps):')
                        problem.print_with_assigned_variables(assigned_vars)
                del assigned_vars[var]
        return None

    @classmethod
    def bt_fc_search(cls, problem: Problem):
        cls._solutions_count = 0
        cls._steps_count = 0
        cls._bt_fc_search({}, problem.variables, problem.domains, problem)

