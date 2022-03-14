# Facility Layout Optimization.
from pathlib import Path

from si_project.flo import FacilityLoader,  Facility, GeneticAlgorithm

if __name__ == '__main__':
    root_path = Path(__file__).parent.parent.resolve()
    assets_path = root_path / 'assets'

    # Load easy facility
    easy_cost_path = assets_path / 'flo_dane_v1.2' / 'easy_cost.json'
    easy_flow_path = assets_path / 'flo_dane_v1.2' / 'easy_flow.json'
    facility: Facility = FacilityLoader.load_facility(
        dimensions=(3, 3),
        machines_count=9,
        flow_file_path=easy_flow_path,
        costs_file_path=easy_cost_path)

    ga = GeneticAlgorithm(
        population_size=1000,
        facility=facility,
        tournament_size=50,
        mutation_prob=0.1,
        selection_size=150)

    ga.run(number_of_generations=1000)
