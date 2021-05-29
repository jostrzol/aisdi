from typing import TextIO, List, Tuple

import argparse
import sys
import string

from rich.console import Console

console = Console(color_system="truecolor")


# Typing Alias
Point = List[int]


class Graph:
    """
    Class representing a graph
    """

    def __init__(self, graph: List[List] = [[]]) -> None:
        """
        Initializes a Graph object

        If no graph is passed to __init__,
        defaults the graph's data to:

        self._graph = [[[0, 0, 1], [0, 0, 1]]]
        self._heigh = 1
        self._width = 2
        self._start = (0, 0)
        self._finish = (1, 0)
        """
        self._graph = graph
        if self._graph == [[]]:
            self._graph[0].append([0, float('inf'), 0])
            self._graph[0].append([0, float('inf'), 0])
        else:
            temp_graph = []
            graph_line = []
            for line in graph:
                for char in line:
                    if str(char) in string.digits:
                        graph_line.append([char, float('inf'), 0])
                temp_graph.append(graph_line)
                graph_line = []
            self._graph = temp_graph
        self._height = 0
        self._width = 0
        self._start = (0, 0)
        self._finish = (0, 0)
        self.dijkstra()

    def make_graph_from_file(self, file: TextIO) -> None:
        """
        Creates a list representation of
        a graph from a file input:

        1034
        5670

        becomes

        [[1, 0, 3, 4],
         [5, 6, 7, 0]]

        or rather

        [[[1, inf, 0], [0,  0,  0], [3, inf, 0], [4, inf, 0]],
         [[5, inf, 0], [6, inf, 0], [7, inf, 0], [0, inf, 0]]]

        where inf = float('inf')
        """
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
        """
        Calculates the dimensions of a rectangular graph:

        [1, 2, 3]
        [4, 5, 6]
        [7, 8, 9]      ==>  graph._height = 3, graph._width = 3

        [1, 2]
        [3, 4]
        [5, 6]
        [7, 8]         ==>  graph._height = 4, graph._width = 2

        [1, 2, 3, 4]
        [5, 6, 7, 8]   ==>  graph._height = 2, graph._width = 4
        """
        self._height = len(self._graph)
        self._width = len(self._graph[0])

    def print_list(self) -> None:
        """
        Prints a graph with all its hidden values
        """
        for line in self._graph:
            print(line)

    def print_point_cost(self) -> None:
        """
        Prints only the cost of individual points
        """
        for line in self._graph:
            for point in line:
                print(point[0], end=" ")
            print()

    def print_total_cost(self) -> None:
        """
        Prints the total cost of getting to
        a specific point from the starting point
        """
        for line in self._graph:
            for point in line:
                print(point[1], end=" ")
            print()

    def print_visit_check(self) -> None:
        """
        Prints whether or not the dijkstra
        algorithm has visited a specific point
        """
        for line in self._graph:
            for point in line:
                print(point[2], end=" ")
            print()

    def find_start_finish(self) -> List[Point]:
        """
        Return the positions of start and finish points:

        [[start_x, start_y], [finish_x, finish_y]]
        """
        start_finish = []
        for y in range(self._height):
            for x in range(self._width):
                if self._graph[y][x][0] == 0:
                    if len(start_finish) == 0:
                        self._graph[y][x][1] = 0
                    start_finish.append((x, y))
        return start_finish

    def dijkstra(self) -> None:
        """
        Utilizes Dijkstra's algorithm to assign
        each point (but not all of them; only these
        we need to get to the finish) on the graph
        a total cost of getting to that specific
        point from the start
        """
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
        """
        Returns the start -> finish path by
        reversing through the lowest cost neighbours,
        starting at the finish point
        """
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
        """
        Prints only those points on the graph
        which are part of the start -> finish path
        """
        path_list = self.return_path()
        for y in range(self._height):
            for x in range(self._width):
                if (x, y) in path_list:
                    print(self._graph[y][x][0], end=" ")
                else:
                    print(end="  ")
            print()

    def pretty_print_path(self) -> None:
        """
        Kinda like print_path(), but with pretty colors
        """
        r = 205
        g = 49
        b = 49
        path_list = self.return_path()
        num_of_points = len(path_list)
        delta_rgb = 156 / num_of_points
        for y in range(self._height):
            for x in range(self._width):
                if (x, y) in path_list:
                    index = path_list.index((x, y))
                    for i in range(index):
                        r -= delta_rgb
                        g += delta_rgb
                        b += delta_rgb
                    color = (int(r), int(g), int(b))
                    hex_color = rgb_to_hex(color)
                    console.print(f"[{hex_color}]{self._graph[y][x][0]}[/]",
                                  end=" ")
                    r = 205
                    g = 49
                    b = 49
                else:
                    console.print(f"[#000000]{self._graph[y][x][0]}[/]",
                                  end=" ")
            print()


def rgb_to_hex(rgb_color: Tuple[int, int, int]):
    hex_color = "#"
    for i in range(3):
        if len(hex(rgb_color[i])[2:]) == 1:
            hex_color += "0"
            hex_color += hex(rgb_color[i])[2:]
        else:
            hex_color += hex(rgb_color[i])[2:]
    return hex_color


def modify_color_value(color_value: int, increase: bool):
    pass


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
    print()
    graph.pretty_print_path()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
