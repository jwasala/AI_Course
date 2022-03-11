from dataclasses import dataclass
from random import randrange

from .facility import Facility


@dataclass
class FacilityLayout:
    """
    Represents a Facility layout (solution to FLO problem).
    """
    layout: list[tuple[int, int]]
    dimensions: tuple[int, int]

    @property
    def width(self) -> int:
        return self.dimensions[0]

    @property
    def height(self) -> int:
        return self.dimensions[1]

    @classmethod
    def random(cls, dimensions, machines_count) -> 'FacilityLayout':
        """
        :param dimensions: width and height of the facility
        :param machines_count: number of machines
        :return: FacilityLayout containing random compatible layout
        """
        width, height = dimensions
        layout = []
        for machine in range(machines_count):
            while True:
                x, y = randrange(0, width), randrange(0, height)
                if (x, y) not in layout:
                    layout.append((x, y))
                    break
        return FacilityLayout(layout, dimensions)

    def fitness(self, facility: Facility) -> int:
        """
        :param facility: Facility object
        :return: value of fitness function for a given facility and layout
        """
        if (facility.width, facility.height) != (self.width, self.height):
            raise ValueError('Facility and FacilityLayout have incompatible '
                             'dimensions')
        total = 0
        for i in range(facility.machines_count):
            for j in range(i + 1, facility.machines_count):
                x_i, y_i = self.layout[i]
                x_j, y_j = self.layout[j]
                dist = abs(x_i - x_j) + abs(y_i - y_j)
                total += facility.flows[i][j] * facility.costs[i][j] * dist
        return total
