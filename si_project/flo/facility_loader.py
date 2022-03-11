from json import load
from pathlib import Path

from .facility import Facility


class FacilityLoader:
    @classmethod
    def _load_from_file_generic(cls,
                                file_path: Path,
                                machines_count: int,
                                value_key: str) -> list[list[int]]:
        machines = range(machines_count)
        data = [[0 for _ in machines] for _ in machines]
        with open(file_path) as flows_file:
            flows_raw: list[dict] = load(flows_file)
            for flow_raw in flows_raw:
                source = flow_raw['source']
                dest = flow_raw['dest']
                amount = flow_raw[value_key]
                data[source][dest] = amount
                data[dest][source] = amount
        return data

    @classmethod
    def _load_flows_from_file(cls,
                              flows_path: Path,
                              machines_count: int) -> list[list[int]]:
        return cls._load_from_file_generic(
            file_path=flows_path,
            machines_count=machines_count,
            value_key='amount')

    @classmethod
    def _load_costs_from_file(cls,
                              costs_path: Path,
                              machines_count: int) -> list[list[int]]:
        return cls._load_from_file_generic(
            file_path=costs_path,
            machines_count=machines_count,
            value_key='cost')

    @classmethod
    def load_facility(cls,
                      dimensions: tuple[int, int],
                      machines_count: int,
                      flow_file_path: Path,
                      costs_file_path: Path) -> Facility:
        """
        :param dimensions: width and height of the facility
        :param machines_count: number of machines
        :param flow_file_path: path to a JSON file containing flow data
        :param costs_file_path: path to a JSON file containing costs data
        :return: Facility object
        """
        width, height = dimensions
        if machines_count > width * height:
            raise ValueError('There are too many machines to fit')
        flows = cls._load_flows_from_file(flow_file_path, machines_count)
        costs = cls._load_costs_from_file(costs_file_path, machines_count)
        return Facility(dimensions, machines_count, flows, costs)
