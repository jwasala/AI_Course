from random import choice

from si_project.flo import FacilityLayout, Facility
from si_project.flo.population import Population


class GeneticAlgorithm:
    def __init__(self, population_size: int, facility: Facility,
                 tournament_size: int, mutation_prob: float,
                 selection_size: int):
        """
        Constructor generates initial random population.
        """
        self.facility = facility
        self.population_size = population_size
        self.tournament_size = tournament_size
        self.mutation_prob = mutation_prob
        self.selection_size = selection_size
        layouts: list[FacilityLayout] = []
        for _ in range(population_size):
            layouts.append(FacilityLayout.random(facility.dimensions,
                                                 facility.machines_count))
        self.generations: list[Population] = [Population(layouts, facility)]

    def create_new_generation(self) -> None:
        """
        Replaces current population with new one by using GA operators.
        """
        last_generation = self.generations[-1]

        # Pick from last generation
        # selected_layouts: list[FacilityLayout] = []
        # while len(selected_layouts) < self.selection_size:
        # selection = last_generation.roulette_selection()
        # selection = last_generation.tournament_selection(self.tournament_size)
        # if selection not in selected_layouts:
        #     selected_layouts.append(selection)
        selected_layouts: list[FacilityLayout] = last_generation\
            .tournament_selection(self.tournament_size)

        # Generate children
        children: list[FacilityLayout] = []
        while len(children) < self.population_size:
            parent = choice(selected_layouts)
            other_parent = choice(selected_layouts)
            child = last_generation.crossover(parent, other_parent)
            children.append(child)
            if len(children) >= self.population_size:
                break

        # Mutate
        new_generation = Population(children, self.facility)
        new_generation = new_generation.mutation(self.mutation_prob)
        self.generations.append(new_generation)

    def run(self, number_of_generations: int):
        if len(self.generations) > 1:
            raise ValueError('Algorithm can be run only once')
        i = 0
        try:
            while True:
                avg = self.generations[-1].avg_fitness
                best = self.generations[-1].best_layout.fitness(self.facility)
                self.create_new_generation()
                # if len(self.generations) >= 2 and \
                #         self.generations[-1].avg_fitness \
                #         > self.generations[-2].avg_fitness:
                #     self.generations.pop()
                # else:
                print(f'Generation {i}, avg = {avg}, best = {best}')
                i += 1
        except KeyboardInterrupt as ke:
            print('Interrupted')
            exit(1)
