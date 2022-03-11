from dataclasses import dataclass

from si_project.flo import FacilityLayout, Facility


@dataclass
class Population:
    """
    Represents a generation of genotypes (FacilityLayouts) in the
    genetic algorithm.
    """
    layouts: list[FacilityLayout]
    facility: Facility

    def merge(self, other: 'Population') -> 'Population':
        if self.facility is not other.facility:
            raise ValueError('Cannot merge populations related to different '
                             'facilities')
        return Population(self.layouts + other.layouts, self.facility)

    def tournament_selection(self, size: int) -> FacilityLayout:
        pass

    def roulette_selection(self) -> FacilityLayout:
        pass

    @staticmethod
    def crossover(parent1: FacilityLayout,
                  parent2: FacilityLayout,
                  children_count: int) -> 'Population':
        pass

    def mutation(self, pm: float) -> 'Population':
        pass
