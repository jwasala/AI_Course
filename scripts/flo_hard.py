# Facility Layout Optimization.
from pathlib import Path

from si_project.flo import FacilityLoader, Facility, GeneticAlgorithm

if __name__ == '__main__':
    root_path = Path(__file__).parent.parent.resolve()
    assets_path = root_path / 'assets'

    # Load easy facility
    easy_cost_path = assets_path / 'flo_dane_v1.2' / 'hard_cost.json'
    easy_flow_path = assets_path / 'flo_dane_v1.2' / 'hard_flow.json'
    facility: Facility = FacilityLoader.load_facility(
        dimensions=(5, 6),
        machines_count=24,
        flow_file_path=easy_flow_path,
        costs_file_path=easy_cost_path)

    ga = GeneticAlgorithm(
        population_size=2000,
        facility=facility,
        tournament_size=100,
        mutation_prob=0.05,
        selection_size=500)

    ga.run(100)
