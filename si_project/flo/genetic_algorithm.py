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
        selected_layouts: list[FacilityLayout] = []
        # while len(selected_layouts) < self.selection_size:
        #     selection = last_generation.roulette_selection()
        #     if selection not in selected_layouts:
        #         selected_layouts.append(selection)
        selected_layouts: list[FacilityLayout] = last_generation \
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

    def run(self, generations: int):
        best_all_time = None
        try:
            for i in range(generations):
                avg = self.generations[-1].avg_fitness
                best = self.generations[-1].best_layout
                if not best_all_time or best_all_time.fitness(self.facility) > best.fitness(self.facility):
                    best_all_time = best
                worst = self.generations[-1].worst_layout.fitness(
                    self.facility)
                std = self.generations[-1].std_fitness
                self.create_new_generation()
                print(f'Generation {i}, avg = {avg}, best = '
                      f'{best.fitness(self.facility)}, worst = {worst}, std = '
                      f'{std}, best_all_time = '
                      f'{best_all_time.fitness(self.facility)}')
                i += 1
        except KeyboardInterrupt as ke:
            print('Interrupted')
            exit(1)
        print(f'{best_all_time.fitness(self.facility)} {best_all_time.layout}')
        return best_all_time

    def run_random(self, iterations: int):
        best: FacilityLayout = None
        for i in range(iterations):
            random_layout = FacilityLayout.random(self.facility.dimensions,
                                                  self.facility.machines_count)
            if not best or best.fitness(self.facility) > random_layout.fitness(self.facility):
                best = random_layout
        print(f'{best.fitness(self.facility)} {best.layout}')
        return best
