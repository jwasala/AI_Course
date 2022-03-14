# Facility Layout Optimization.
from pathlib import Path

from si_project.flo import FacilityLoader, FacilityLayout, Facility, \
    GeneticAlgorithm

if __name__ == '__main__':
    root_path = Path(__file__).parent.parent.resolve()
    assets_path = root_path / 'assets'

    # Load easy facility
    easy_cost_path = assets_path / 'flo_dane_v1.2' / 'flat_cost.json'
    easy_flow_path = assets_path / 'flo_dane_v1.2' / 'flat_flow.json'
    facility: Facility = FacilityLoader.load_facility(
        dimensions=(1, 12),
        machines_count=12,
        flow_file_path=easy_flow_path,
        costs_file_path=easy_cost_path)

    ga = GeneticAlgorithm(
        population_size=200,
        facility=facility,
        tournament_size=5,
        mutation_prob=0.25,
        selection_size=30)

    ga.run(number_of_generations=1000)
