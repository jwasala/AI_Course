from copy import copy
from datetime import datetime
from typing import Generic, Callable

from .problem import Problem, VLabel, VValue


class BTFCSearch(Generic[VLabel, VValue]):
    _solutions_count = 0
    _steps_count = 0
    _time = datetime.now()
    _solutions = set()

    @classmethod
    def _bt_fc_search(cls,
                      assigned_vars: list[tuple[VLabel, VValue]],
                      unassigned_vars: list[VLabel],
                      domain: dict[VLabel, list[VValue]],
                      problem: Problem):
        if cls._solutions_count != 0:
            return
        if not unassigned_vars:
            return tuple(assigned_vars)
        var, unassigned_vars = unassigned_vars[0], unassigned_vars[1:]
        for val in domain[var]:
            cls._steps_count += 1
            if assigned_vars or problem.check_constraints((var, val), {k: v for k, v in assigned_vars}):
                assigned_vars.append((var, val))
                domain_cp = copy(domain)
                neighbors = problem.neighbors_of(var)
                for var_y in unassigned_vars:
                    if (var_y, var) in problem.constraints or (var, var_y) in problem.constraints:
                        domain_cp[var_y] = [val_y for val_y in domain_cp[var_y] if
                                            problem.check_constraints_between((var, val), (var_y, val_y))]
                if all(domain_cp[var_y] for var_y in neighbors):
                    result = cls._bt_fc_search(assigned_vars, unassigned_vars, domain_cp, problem)
                    if result and str(result) not in cls._solutions:
                        cls._solutions.add(str(result))
                        cls._solutions_count += 1
                        print('BT+FC', cls._solutions_count, cls._steps_count,
                              (datetime.now() - cls._time).total_seconds())
                        # problem.print_with_assigned_variables(assigned_vars)
                assigned_vars.pop()
        return None

    @classmethod
    def bt_fc_search(cls,
                     problem: Problem,
                     order_vars: Callable[[Problem], list[VLabel]] = None,
                     order_domains: Callable[[Problem], dict[VLabel, list[VValue]]] = None):
        cls._solutions_count = 0
        cls._steps_count = 0
        cls._time = datetime.now()
        print(f'BT+FC, {order_vars}, {order_domains}')
        cls._bt_fc_search([],
                          order_vars(problem) if order_vars else problem.variables,
                          order_domains(problem) if order_domains else problem.domains,
                          problem)
        print(cls._steps_count)
