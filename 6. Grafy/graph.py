from __future__ import annotations
from typing import Optional, TextIO, List, Tuple, Union
from copy import copy

import argparse
import sys
import string

from dataclasses import dataclass

from rich.console import Console

console = Console(color_system="truecolor")


@dataclass
class Point:
    weight: int
    cost: int = float('inf')
    visited: bool = False

    def __str__(self):
        return "{" + f'w:{self.weight},c:{self.cost},v:{self.visited}' + "}"


@dataclass
class Position:
    x: int
    y: int

    def neighbours(self, bounds: Optional[Rectangle] = None):
        """
        yields all neighbouring positions which fit in the rectangle given
        """
        d = (-1, 1)
        for dx in d:
            pos = Position(self.x + dx, self.y)
            if bounds is None or bounds.fits(pos):
                yield pos
        for dy in d:
            pos = Position(self.x, self.y + dy)
            if bounds is None or bounds.fits(pos):
                yield pos

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


@dataclass
class Rectangle:
    _bl: Position
    _tr: Position

    def __post_init__(self):
        if self._bl.x > self._tr.x:
            tmp = self._bl.x
            self._bl.x = self._tr.x
            self._tr.x = tmp
        if self._bl.y > self._tr.y:
            tmp = self._bl.y
            self._bl.y = self._tr.y
            self._tr.y = tmp

    def fits(self, position: Position) -> True:
        """
        Checks if position fits inside the square
        """
        return position.x >= self._bl.x and position.y >= self._bl.y and \
            position.x <= self._tr.x and position.y <= self._tr.y


class Graph:
    """
    Class representing a graph
    """

    def __init__(self, graph: Union[List[List[int]], TextIO] = None) -> None:
        """
        Initializes a Graph object

        If no graph is passed to __init__,
        defaults the graph's data to:

        self._graph = [[[0, 0, false], [0, inf, false]]]
        self._heigh = 1
        self._width = 2
        self._start = (0, 0)
        self._finish = (1, 0)
        """
        if graph is None:
            graph = [[0, 0]]

        self._graph: List[List[Point]] = []
        for line in graph:
            graph_line: List[Point] = []
            for char in line:
                if str(char) in string.digits:
                    graph_line.append(Point(int(char)))
            self._graph.append(graph_line)

        self._height = len(self._graph)
        self._width = len(self._graph[0])

        self._bounds = Rectangle(
            Position(0, 0), Position(self._width-1, self._height-1))

        self._start, self._finish = self.find_start_finish()

    def print_list(self) -> None:
        """
        Prints a graph with all its hidden values
        """
        for line in self._graph:
            print(line)

    def print_point_weight(self) -> None:
        """
        Prints only the weight of individual points
        """
        for line in self._graph:
            for point in line:
                print(point.weight, end=" ")
            print()

    def print_total_cost(self) -> None:
        """
        Prints the total cost of getting to
        a specific point from the starting point
        """
        for line in self._graph:
            for point in line:
                print(point.cost, end=" ")
            print()

    def print_visit_check(self) -> None:
        """
        Prints whether or not the dijkstra
        algorithm has visited a specific point
        """
        for line in self._graph:
            for point in line:
                to_print = 0
                if point.visited:
                    to_print = 1
                print(to_print, end=" ")
            print()

    def find_start_finish(self) -> Tuple[Position, Position]:
        """
        Return the positions of start and finish points:

        ((start_x, start_y), (finish_x, finish_y))
        """
        start: Position = None
        finish: Position = None

        for pos in self:
            p = self._get(pos)
            if p.weight == 0:
                if start is None:
                    p.cost = 0
                    start = copy(pos)
                else:
                    finish = pos
        return start, finish

    def _get(self, position: Position) -> Point:
        """
        Returns a point under the given position
        """
        return self._graph[position.y][position.x]

    def dijkstra(self) -> None:
        """
        Utilizes Dijkstra's algorithm to assign
        each point (but not all of them; only these
        we need to get to the finish) on the graph
        a total cost of getting to that specific
        point from the start
        """
        c_p_pos = self._start       # current_point_pos
        c_p = self._get(c_p_pos)    # current_point
        reached_finish = False
        while(not reached_finish):
            for pos in c_p_pos.neighbours(self._bounds):
                p = self._get(pos)
                if not p.visited and c_p.cost + p.weight < p.cost:
                    p.cost = c_p.cost + p.weight

            c_p.visited = True

            min_cost = float('inf')
            min_cost_pos = Position(0, 0)
            for pos in self:
                p = self._get(pos)
                if not p.visited and p.cost < min_cost:
                    min_cost_pos = pos
                    min_cost = p.cost

            c_p_pos = min_cost_pos
            c_p = self._get(min_cost_pos)

            if self._get(self._finish).visited:
                reached_finish = True

    def return_path(self) -> List[Position]:
        """
        Returns the start -> finish path by
        reversing through the lowest cost neighbours,
        starting at the finish point
        """
        path_list: List[Position] = []
        c_p_pos = self._finish          # current_point_pos
        reached_start = False
        while(not reached_start):
            path_list.append(c_p_pos)
            min_val = float('inf')
            next_point_pos: Position

            for pos in c_p_pos.neighbours(self._bounds):
                p = self._get(pos)
                if p.cost < min_val:
                    min_val = p.cost
                    next_point_pos = pos

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
                pos = Position(x, y)
                if pos in path_list:
                    print(self._get(pos).weight, end=" ")
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
                pos = Position(x, y)
                p = self._get(pos)
                if pos in path_list:
                    index = path_list.index(pos)
                    r -= delta_rgb * index
                    g += delta_rgb * index
                    b += delta_rgb * index
                    color = (int(r), int(g), int(b))
                    hex_color = rgb_to_hex(color)
                    console.print(f"[{hex_color}]{p.weight}[/]",
                                  end=" ")
                    r = 205
                    g = 49
                    b = 49
                else:
                    console.print(f"[#000000]{p.weight}[/]",
                                  end=" ")
            print()

    def __iter__(self):
        self._current = Position(0, 0)
        return self

    def __next__(self):
        tmp = copy(self._current)
        self._current.x += 1
        if not self._bounds.fits(tmp):
            raise StopIteration
        elif not self._bounds.fits(self._current):
            self._current.x = 0
            self._current.y += 1
        return tmp


def rgb_to_hex(rgb_color: Tuple[int, int, int]):
    hex_color = "#"
    for i in range(3):
        if len(hex(rgb_color[i])[2:]) == 1:
            hex_color += "0"
            hex_color += hex(rgb_color[i])[2:]
        else:
            hex_color += hex(rgb_color[i])[2:]
    return hex_color


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="find a path in a graph")
    parser.add_argument("file", type=argparse.FileType("r"),
                        nargs="?",
                        default=sys.stdin,
                        help="a path to the file containing the graph")
    args = parser.parse_args(argv)
    graph = Graph(args.file)
    graph.dijkstra()
    # graph.print_point_weight()
    # print()
    graph.print_path()
    # print()
    # graph.pretty_print_path()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
