from typing import Tuple, List

import argparse
import sys
import string


# Type Alias
Point = Tuple[int, int]


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="find a path in a graph")
    parser.add_argument("file", type=argparse.FileType("r"),
                        nargs="?",
                        default=sys.stdin,
                        help="a path to the file containing the graph")
    args = parser.parse_args(argv)

    # test argparse system
    # ".\graph.py .\graphs\graph10x10.txt" should do just fine
    graph = []
    graph_line = []
    for line in args.file:
        for char in line:
            if char in string.digits:
                graph_line.append(int(char))
        graph.append(graph_line)
        graph_line = []
    print(graph)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
