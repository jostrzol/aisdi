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
        c_p_pos = self._start                       # current_point_pos
        c_p = self._graph[c_p_pos[1]][c_p_pos[0]]   # current_point
        reached_finish = False
        while(not reached_finish):
            if c_p_pos[0] != 0:
                if self._graph[c_p_pos[1]][c_p_pos[0] - 1][2] == 0:
                    if c_p[1] + self._graph[c_p_pos[1]][c_p_pos[0] - 1][0] < \
                       self._graph[c_p_pos[1]][c_p_pos[0] - 1][1]:
                        self._graph[c_p_pos[1]][c_p_pos[0] - 1][1] = c_p[1] + \
                            self._graph[c_p_pos[1]][c_p_pos[0] - 1][0]

            if c_p_pos[0] != (self._width - 1):
                if self._graph[c_p_pos[1]][c_p_pos[0] + 1][2] == 0:
                    if c_p[1] + self._graph[c_p_pos[1]][c_p_pos[0] + 1][0] < \
                       self._graph[c_p_pos[1]][c_p_pos[0] + 1][1]:
                        self._graph[c_p_pos[1]][c_p_pos[0] + 1][1] = c_p[1] + \
                            self._graph[c_p_pos[1]][c_p_pos[0] + 1][0]

            if c_p_pos[1] != 0:
                if self._graph[c_p_pos[1] - 1][c_p_pos[0]][2] == 0:
                    if c_p[1] + self._graph[c_p_pos[1] - 1][c_p_pos[0]][0] < \
                       self._graph[c_p_pos[1] - 1][c_p_pos[0]][1]:
                        self._graph[c_p_pos[1] - 1][c_p_pos[0]][1] = c_p[1] + \
                            self._graph[c_p_pos[1] - 1][c_p_pos[0]][0]

            if c_p_pos[1] != (self._height - 1):
                if self._graph[c_p_pos[1] + 1][c_p_pos[0]][2] == 0:
                    if c_p[1] + self._graph[c_p_pos[1] + 1][c_p_pos[0]][0] < \
                       self._graph[c_p_pos[1] + 1][c_p_pos[0]][1]:
                        self._graph[c_p_pos[1] + 1][c_p_pos[0]][1] = c_p[1] + \
                            self._graph[c_p_pos[1] + 1][c_p_pos[0]][0]

            c_p[2] = 1

            min_cost = float('inf')
            min_cost_pos = (0, 0)
            for y in range(self._height):
                for x in range(self._width):
                    if self._graph[y][x][1] < min_cost and \
                       self._graph[y][x][2] == 0:
                        min_cost_pos = (x, y)
                        min_cost = self._graph[y][x][1]

            c_p_pos = min_cost_pos
            c_p = self._graph[c_p_pos[1]][c_p_pos[0]]

            if self._graph[self._finish[1]][self._finish[0]][2] == 1:
                reached_finish = True

    def return_path(self) -> List[Point]:
        path_list = []
        c_p_pos = self._finish                      # current_point_pos
        reached_start = False
        while(not reached_start):
            path_list.append(c_p_pos)
            min_val = float('inf')
            next_point_pos = (0, 0)
            if c_p_pos[0] != 0:
                if self._graph[c_p_pos[1]][c_p_pos[0] - 1][1] < min_val:
                    min_val = self._graph[c_p_pos[1]][c_p_pos[0] - 1][1]
                    next_point_pos = (c_p_pos[0] - 1, c_p_pos[1])

            if c_p_pos[0] != (self._width - 1):
                if self._graph[c_p_pos[1]][c_p_pos[0] + 1][1] < min_val:
                    min_val = self._graph[c_p_pos[1]][c_p_pos[0] + 1][1]
                    next_point_pos = (c_p_pos[0] + 1, c_p_pos[1])

            if c_p_pos[1] != 0:
                if self._graph[c_p_pos[1] - 1][c_p_pos[0]][1] < min_val:
                    min_val = self._graph[c_p_pos[1] - 1][c_p_pos[0]][1]
                    next_point_pos = (c_p_pos[0], c_p_pos[1] - 1)

            if c_p_pos[1] != (self._height - 1):
                if self._graph[c_p_pos[1] + 1][c_p_pos[0]][1] < min_val:
                    min_val = self._graph[c_p_pos[1] + 1][c_p_pos[0]][1]
                    next_point_pos = (c_p_pos[0], c_p_pos[1] + 1)

            c_p_pos = next_point_pos

            if c_p_pos == self._start:
                path_list.append(self._start)
                reached_start = True

        path_list.reverse()
        return(path_list)

    def print_path(self) -> None:
        path_list = self.return_path()
        for y in range(self._height):
            for x in range(self._width):
                if (x, y) in path_list:
                    print(self._graph[y][x][0], end=" ")
                else:
                    print(end="  ")
            print()


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="find a path in a graph")
    parser.add_argument("file", type=argparse.FileType("r"),
                        nargs="?",
                        default=sys.stdin,
                        help="a path to the file containing the graph")
    args = parser.parse_args(argv)
    graph = Graph()
    graph.make_graph_from_file(args.file)
    graph.dijkstra()
    graph.print_point_cost()
    print()
    graph.print_path()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
