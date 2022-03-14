from dataclasses import dataclass
from random import choice, uniform, random, randrange

from si_project.flo import FacilityLayout, Facility


@dataclass
class Population:
    """
    Represents a generation of genotypes (FacilityLayouts) in the
    genetic algorithm.
    """
    layouts: list[FacilityLayout]
    facility: Facility

    @property
    def best_layout(self) -> FacilityLayout:
        """
        :return: best FacilityLayout (by lowest fitness value).
        """
        return min(self.layouts,
                   key=lambda layout: layout.fitness(self.facility))

    @property
    def avg_fitness(self) -> float:
        return sum([layout.fitness(self.facility) for layout in
                    self.layouts]) / len(self.layouts)

    def merge(self, other: 'Population') -> 'Population':
        if self.facility is not other.facility:
            raise ValueError('Cannot merge populations related to different '
                             'facilities')
        return Population(self.layouts + other.layouts, self.facility)

    def tournament_selection(self, size: int) -> list[FacilityLayout]:
        def split(a, n):
            k, m = divmod(len(a), n)
            return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in
                    range(n))

        if size <= 0:
            raise ValueError('Size of tournament selection cannot be 0 or '
                             'less')
        if size > len(self.layouts):
            raise ValueError('Size of tournament selection cannot be greater '
                             'than population count')
        groups = split(self.layouts, size)
        selections = [
            min(candidates,
                key=lambda layout: layout.fitness(self.facility)) for
            candidates in groups]
        return selections

    def roulette_selection(self) -> FacilityLayout:
        fits = [1 / layout.fitness(self.facility) for layout in self.layouts]
        pick = uniform(0, sum(fits))
        for i, fit in enumerate(fits):
            pick -= fit
            if pick <= 0:
                return self.layouts[i]

    def crossover(self, parent1: FacilityLayout,
                  parent2: FacilityLayout) -> FacilityLayout:
        if len(parent1.layout) != len(parent2.layout):
            raise ValueError('Parents with different number of machines '
                             'cannot crossover')
        if parent1.dimensions != parent2.dimensions:
            raise ValueError('Parents with different dimensions cannot '
                             'crossover')
        child_layout: list[tuple[int, int]] = []
        for pos1, pos2 in zip(parent1.layout, parent2.layout):
            if pos1 in child_layout and pos2 in child_layout:
                while True:
                    x = randrange(0, self.facility.width)
                    y = randrange(0, self.facility.height)
                    if (x, y) not in child_layout:
                        child_layout.append((x, y))
                        break
            elif pos1 in child_layout and pos2 not in child_layout:
                child_layout.append(pos2)
            elif pos1 not in child_layout and pos2 in child_layout:
                child_layout.append(pos1)
            else:
                child_layout.append(choice([pos1, pos2]))
        return FacilityLayout(child_layout, parent1.dimensions)

    def mutation(self, prob: float) -> 'Population':
        for layout in [layout.layout for layout in self.layouts]:
            if random() < prob:
                rand1 = randrange(0, len(layout))
                rand2 = randrange(0, len(layout))
                layout[rand1], layout[rand2] = layout[rand2], layout[rand1]
        return Population(self.layouts, self.facility)
