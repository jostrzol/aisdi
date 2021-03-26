from typing import Callable

import algorithms

test_filename = "reference/lorem_ipsum.txt"
desired_filename = "reference/lorem_ipsum_sorted.txt"


def algorithm_test(func: Callable[[list], list]):
    result = []
    with open(test_filename, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            line = "".join(func([char for char in line]))
            result.append(line + "\n")
    with open(desired_filename, "r") as f:
        assert f.readlines() == result


def test_quicksort():
    algorithm_test(algorithms.quicksort)


def test_bubblesort():
    algorithm_test(algorithms.bubblesort)


def test_mergesort():
    algorithm_test(algorithms.mergesort)


def test_countsort():
    algorithm_test(algorithms.countsort)
