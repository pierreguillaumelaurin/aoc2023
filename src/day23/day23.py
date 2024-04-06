from collections import deque
from typing import Dict, List

from src.coordinates import Coordinates, substract_coordinates
from src.utils import benchmark


def parsed_input():
    with open("./input.dat", "r") as data:
        return [line.strip() for line in data.readlines()]


SLOPES = ["^", ">", "v", "<"]
WALKABLE_TILES = ["."] + SLOPES


class WeightedGraph:
    class Edge:
        def __init__(self, source: Coordinates, destination: Coordinates, weight: int):
            self.source = source
            self.destination = destination
            self.weight = weight

        def __repr__(self):
            return (
                f"Edge<from:{self.source}, to:{self.destination}, weight:{self.weight}>"
            )

    def __init__(self, trails_map: List[str]):
        self._trails_map = trails_map
        self.nodes = set()
        self.edges = []

        self.start = (0, trails_map[0].index("."))
        self.end = (len(trails_map) - 1, trails_map[len(trails_map) - 1].index("."))

        self.nodes.add(self.start)
        self.nodes.add(self.end)
        self._add_nodes()

        self._add_edges()

    def _add_nodes(self):
        for i in range(len(self._trails_map)):
            for j in range(len(self._trails_map[i])):
                if self._trails_map[i][j] == "#":
                    continue
                position = (i, j)
                walkable_adjacent_cells = self.get_walkable_adjacent_slopes(position)
                match len(walkable_adjacent_cells):
                    case 0 | 1:
                        continue
                    case 2:
                        self.nodes.add(position)
                    case _:
                        raise Exception(
                            "unexpected length", walkable_adjacent_cells, position
                        )

    def _add_edges(self):
        for node in self.nodes:
            stack = [(node, 0)]
            seen = {node}

            while stack:
                position, count = stack.pop()

                if position in self.nodes and count != 0:
                    edge = WeightedGraph.Edge(
                        source=node, destination=position, weight=count
                    )
                    self.edges.append(edge)
                else:
                    for cell in self.get_walkable_adjacent_cells(position):
                        if cell not in seen:
                            stack.append((cell, count + 1))
                            seen.add(cell)

    def topological_sort(self):
        result = deque()
        seen = set()

        def helper(node: Coordinates):
            neighbors = [
                _edge.destination for _edge in self.edges if _edge.source == node
            ]
            for neighbor in neighbors:
                if neighbor not in seen:
                    seen.add(neighbor)
                    helper(neighbor)
            result.appendleft(node)

        helper(self.start)
        return result

    def find_longest_path(self):
        node_cost_from_start = {node: -float("inf") for node in self.nodes}
        node_cost_from_start[self.start] = 0
        for node in self.topological_sort():
            connections = [edge for edge in self.edges if edge.source == node]
            for connection in connections:
                if (
                    node_cost_from_start[connection.source] + connection.weight
                    > node_cost_from_start[connection.destination]
                ):
                    node_cost_from_start[connection.destination] = (
                        node_cost_from_start[connection.source] + connection.weight
                    )
        return node_cost_from_start[self.end]

    def get_adjacent_cells(self, coordinates: Coordinates):
        x, y = coordinates
        adjacent_cells = ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))
        return [
            (r, c)
            for (r, c) in adjacent_cells
            if 0 <= r < len(self._trails_map) and 0 <= c < len(self._trails_map[0])
        ]

    def get_walkable_adjacent_slopes(self, position: Coordinates):
        walkable_adjacent_slopes = []
        slopes_except_forest = [
            cell
            for cell in self.get_adjacent_cells(position)
            if self._trails_map[cell[0]][cell[1]] in SLOPES
        ]
        for cell in slopes_except_forest:
            tile_value = self._trails_map[cell[0]][cell[1]]
            match substract_coordinates(cell, position):
                case (-1, 0) if tile_value != "v":
                    walkable_adjacent_slopes.append(cell)
                case (0, -1) if tile_value != ">":
                    walkable_adjacent_slopes.append(cell)
                case (1, 0) if tile_value != "^":
                    walkable_adjacent_slopes.append(cell)
                case (0, 1) if tile_value != "<":
                    walkable_adjacent_slopes.append(cell)
                case _:
                    continue
        return walkable_adjacent_slopes

    def get_walkable_adjacent_cells(self, position: Coordinates):
        walkable_adjacent_cells = []
        cells_except_forest = [
            cell
            for cell in self.get_adjacent_cells(position)
            if self._trails_map[cell[0]][cell[1]] in WALKABLE_TILES
        ]
        for cell in cells_except_forest:
            tile_value = self._trails_map[cell[0]][cell[1]]
            match substract_coordinates(cell, position):
                case (-1, 0) if tile_value != "v":
                    walkable_adjacent_cells.append(cell)
                case (0, -1) if tile_value != ">":
                    walkable_adjacent_cells.append(cell)
                case (1, 0) if tile_value != "^":
                    walkable_adjacent_cells.append(cell)
                case (0, 1) if tile_value != "<":
                    walkable_adjacent_cells.append(cell)
                case _:
                    continue
        return walkable_adjacent_cells


@benchmark
def part_one(trails: List[str]):
    graph = WeightedGraph(trails)
    return graph.find_longest_path()


@benchmark
def part_two(trails: List[str]):
    pass


if __name__ == "__main__":
    print(part_one(parsed_input()))
    assert part_one(parsed_input()) == 2170.0
    print(part_two(parsed_input()))
