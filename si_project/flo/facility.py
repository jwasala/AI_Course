from dataclasses import dataclass


@dataclass
class Facility:
    dimensions: tuple[int, int]
    machines_count: int
    flows: list[list[int]]
    costs: list[list[int]]

    @property
    def width(self):
        return self.dimensions[0]

    @property
    def height(self):
        return self.dimensions[1]

    @property
    def machines(self):
        return range(self.machines_count)
