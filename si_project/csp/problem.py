from abc import ABC, abstractmethod
from functools import cached_property, cache
from typing import TypeVar, Generic, Callable

VLabel = TypeVar('VLabel')
VValue = TypeVar('VValue')


class Problem(ABC, Generic[VLabel, VValue]):
    Variable = tuple[VLabel, VValue]

    @cached_property
    @abstractmethod
    def variables(self) -> list[VLabel]:
        pass

    @cached_property
    @abstractmethod
    def domains(self) -> dict[VLabel, list[VValue]]:
        pass

    @cached_property
    @abstractmethod
    def constraints(self) -> dict[tuple[VLabel, VLabel], set[Callable[[Variable, Variable], bool]]]:
        pass

    @cache
    def neighbors_of(self, v: VLabel) -> set[VLabel]:
        return {v2 for v2 in self.variables if (v, v2) in self.constraints and self.constraints[(v, v2)]}

    def check_constraints(self, current_variable: Variable, assigned_variables: dict[VLabel, VValue]):
        current_label, current_val = current_variable
        for neighbor_label in self.neighbors_of(current_label):
            neighbor_val = assigned_variables.get(neighbor_label) or None
            constraints = self.constraints[(current_label, neighbor_label)]
            if neighbor_val:
                if any(not constr(current_variable, (neighbor_label, neighbor_val)) for constr in constraints):
                    return False
        return True

    def check_constraints_between(self, var: Variable, other_var: Variable):
        return all(constr(var, other_var) for constr in self.constraints[(var[0], other_var[0])])

    @abstractmethod
    def print_with_assigned_variables(self, assigned_variables: dict[VLabel, VValue]):
        pass
