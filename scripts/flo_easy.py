# Facility Layout Optimization.
from pathlib import Path
from statistics import stdev

from si_project.flo import FacilityLoader, Facility, GeneticAlgorithm, \
    FacilityLayout

if __name__ == '__main__':
    root_path = Path(__file__).parent.parent.resolve()
    assets_path = root_path / 'assets'

    # Load easy facility
    # easy_cost_path = assets_path / 'flo_dane_v1.2' / 'easy_cost.json'
    # easy_flow_path = assets_path / 'flo_dane_v1.2' / 'easy_flow.json'
    # facility: Facility = FacilityLoader.load_facility(
    #     dimensions=(3, 3),
    #     machines_count=9,
    #     flow_file_path=easy_flow_path,
    #     costs_file_path=easy_cost_path)

    # Load flat facility
    # easy_cost_path = assets_path / 'flo_dane_v1.2' / 'flat_cost.json'
    # easy_flow_path = assets_path / 'flo_dane_v1.2' / 'flat_flow.json'
    # facility: Facility = FacilityLoader.load_facility(
    #     dimensions=(1, 12),
    #     machines_count=12,
    #     flow_file_path=easy_flow_path,
    #     costs_file_path=easy_cost_path)

    # Load hard facility
    easy_cost_path = assets_path / 'flo_dane_v1.2' / 'hard_cost.json'
    easy_flow_path = assets_path / 'flo_dane_v1.2' / 'hard_flow.json'
    facility: Facility = FacilityLoader.load_facility(
        dimensions=(5, 6),
        machines_count=24,
        flow_file_path=easy_flow_path,
        costs_file_path=easy_cost_path)

    results: list[FacilityLayout] = []
    results_random: list[FacilityLayout] = []
    for i in range(10):
        ga = GeneticAlgorithm(
            population_size=1000,
            facility=facility,
            tournament_size=100,
            mutation_prob=0.1,
            selection_size=100)

        results.append(ga.run(80))

    best_result = min(results, key=lambda result: result.fitness(facility))
    # best_random_result = min(results_random,
    #                         key=lambda result: result.fitness(facility))
    worst_result = max(results, key=lambda result: result.fitness(facility))
    # worst_random_result = max(results_random,
    #                          key=lambda result: result.fitness(facility))
    fitnesses = [layout.fitness(facility) for layout in results]
    # fitnesses_random = [layout.fitness(facility) for layout in results_random]
    avg_result = sum(fitnesses) / len(fitnesses)
    # avg_result_random = sum(fitnesses_random) / len(fitnesses_random)
    std_result = stdev(fitnesses)
    # std_result_random = stdev(fitnesses_random)

    print(
        f'Result: best {best_result.fitness(facility)} worst '
        f'{worst_result.fitness(facility)} avg {avg_result} std {std_result} ')
    # print(
    #     f'Result (random): best {best_random_result.fitness(facility)} worst '
    #     f'{worst_random_result.fitness(facility)} avg {avg_result_random} '
    #     f'std {std_result_random}')
