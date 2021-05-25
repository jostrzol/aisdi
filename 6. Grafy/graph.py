from typing import TextIO, List

import argparse
import sys
import string


# Type Alias
Point = List[int]


class Graph:
    def __init__(self, graph: List[List] = [[]]) -> None:
        self._graph = graph
        self._height = len(self._graph)
        if len(graph) > 1:
            self._width = len(self._graph[0])
            self._start = (self.find_start_finish())[0]
            self._finish = (self.find_start_finish())[1]
        else:
            self._width = 0
            self._start = (0, 0)
            self._finish = (0, 0)

    def make_graph_from_file(self, file: TextIO) -> None:
        graph = []
        graph_line = []
        for line in file:
            for char in line:
                if char in string.digits:
                    graph_line.append([int(char), float('inf'), 0])
            graph.append(graph_line)
            graph_line = []
        self._graph = graph
        self.calculate_dimensions()

    def calculate_dimensions(self) -> None:
        self._height = len(self._graph)
        self._width = len(self._graph[0])

    def print_list(self) -> None:
        for line in self._graph:
            print(line)

    def print_point_cost(self) -> None:
        for line in self._graph:
            for point in line:
                print(point[0], end=" ")
            print()

    def print_total_cost(self) -> None:
        for line in self._graph:
            for point in line:
                print(point[1], end=" ")
            print()

    def print_visit_check(self) -> None:
        for line in self._graph:
            for point in line:
                print(point[2], end=" ")
            print()

    def find_start_finish(self) -> List[Point]:
        start_finish = []
        for y in range(self._height):
            for x in range(self._width):
                if self._graph[y][x][0] == 0:
                    if len(start_finish) == 0:
                        self._graph[y][x][1] = 0
                    start_finish.append((x, y))
        return start_finish

    def dijkstra(self) -> None:
        self.calculate_dimensions()
        self._start = (self.find_start_finish())[0]
        self._finish = (self.find_start_finish())[1]
        reached_finish = False
        current_point_pos = self._start
        current_point = self._graph[current_point_pos[1]][current_point_pos[0]]
        while(not reached_finish):
            if current_point_pos[0] != 0:
                if self._graph[current_point_pos[1]][current_point_pos[0] - 1][2] == 0:
                    if current_point[1] + self._graph[current_point_pos[1]][current_point_pos[0] - 1][0] < self._graph[current_point_pos[1]][current_point_pos[0] - 1][1]:
                        self._graph[current_point_pos[1]][current_point_pos[0] - 1][1] = current_point[1] + \
                            self._graph[current_point_pos[1]][current_point_pos[0] - 1][0]

            if current_point_pos[0] != (self._width - 1):
                if self._graph[current_point_pos[1]][current_point_pos[0] + 1][2] == 0:
                    if current_point[1] + self._graph[current_point_pos[1]][current_point_pos[0] + 1][0] < self._graph[current_point_pos[1]][current_point_pos[0] + 1][1]:
                        self._graph[current_point_pos[1]][current_point_pos[0] + 1][1] = current_point[1] + \
                            self._graph[current_point_pos[1]][current_point_pos[0] + 1][0]

            if current_point_pos[1] != 0:
                if self._graph[current_point_pos[1] - 1][current_point_pos[0]][2] == 0:
                    if current_point[1] + self._graph[current_point_pos[1] - 1][current_point_pos[0]][0] < self._graph[current_point_pos[1] - 1][current_point_pos[0]][1]:
                        self._graph[current_point_pos[1] - 1][current_point_pos[0]][1] = current_point[1] + \
                            self._graph[current_point_pos[1] - 1][current_point_pos[0]][0]

            if current_point_pos[1] != (self._height - 1):
                if self._graph[current_point_pos[1] + 1][current_point_pos[0]][2] == 0:
                    if current_point[1] + self._graph[current_point_pos[1] + 1][current_point_pos[0]][0] < self._graph[current_point_pos[1] + 1][current_point_pos[0]][1]:
                        self._graph[current_point_pos[1] + 1][current_point_pos[0]][1] = current_point[1] + \
                            self._graph[current_point_pos[1] + 1][current_point_pos[0]][0]

            current_point[2] = 1

            min_cost = float('inf')
            min_cost_pos = (0, 0)
            for y in range(self._height):
                for x in range(self._width):
                    if self._graph[y][x][1] < min_cost and self._graph[y][x][2] == 0:
                        min_cost_pos = (x, y)
                        min_cost = self._graph[y][x][1]

            current_point_pos = min_cost_pos
            current_point = self._graph[current_point_pos[1]][current_point_pos[0]]

            if self._graph[self._finish[1]][self._finish[0]][2] == 1:
                reached_finish = True


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="find a path in a graph")
    parser.add_argument("file", type=argparse.FileType("r"),
                        nargs="?",
                        default=sys.stdin,
                        help="a path to the file containing the graph")
    args = parser.parse_args(argv)
    graph = Graph()
    graph.make_graph_from_file(args.file)
    graph.print_list()
    print(graph.find_start_finish())
    graph.dijkstra()
    graph.print_list()
    graph.print_point_cost()
    graph.print_total_cost()
    graph.print_visit_check()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
