from dataclasses import dataclass
from typing import Iterable


@dataclass
class Facility:
    """
    Represents a Facility setup (input to FLO problem).
    """
    dimensions: tuple[int, int]
    machines_count: int
    flows: list[list[int]]
    costs: list[list[int]]

    @property
    def width(self) -> int:
        return self.dimensions[0]

    @property
    def height(self) -> int:
        return self.dimensions[1]

    @property
    def machines(self) -> Iterable[int]:
        return range(self.machines_count)
