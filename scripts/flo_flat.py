# Facility Layout Optimization.
from pathlib import Path

from si_project.flo import FacilityLoader, FacilityLayout, Facility

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

    # Random layout
    random_layout = FacilityLayout.random((1, 12), 12)

    # Read fitness value
    print(f'Fitness function value for random layout: '
          f'{random_layout.fitness(facility)}')
