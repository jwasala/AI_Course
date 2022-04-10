from abc import ABC, abstractmethod
from functools import cached_property
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
    def constraints(self) -> dict[tuple[VLabel, VLabel], list[Callable[[Variable, Variable], bool]]]:
        pass

    def check_constraints(self, current_variable: Variable, assigned_variables: dict[VLabel, VValue]):
        current_label, current_val = current_variable
        for other_label, constraints in ((v2, c) for (v1, v2), c in self.constraints.items() if v1 == current_label):
            if other_label in assigned_variables:
                other_val = assigned_variables[other_label]
                if not all(constr(current_variable, (other_label, other_val)) for constr in constraints):
                    return False
        for other_label, constraints in ((v1, c) for (v1, v2), c in self.constraints.items() if v2 == current_label):
            if other_label in assigned_variables:
                other_val = assigned_variables[other_label]
                if not all(constr((other_label, other_val), current_variable) for constr in constraints):
                    return False
        return True

    @abstractmethod
    def print_with_assigned_variables(self, assigned_variables: dict[VLabel, VValue]):
        pass
