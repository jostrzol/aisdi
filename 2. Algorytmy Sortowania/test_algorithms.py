from typing import Callable

import algorithms

test_filename = "reference/lorem_ipsum.txt"


def algorithm_test(func: Callable[[list], list]):
    with open(test_filename, "r") as f:
        for line in f:
            line = line.rstrip("\n")

            got = func([char for char in line])
            want = sorted([char for char in line])

            assert got == want


def test_quicksort():
    algorithm_test(algorithms.quicksort)


def test_bubblesort():
    algorithm_test(algorithms.bubblesort)


def test_mergesort():
    algorithm_test(algorithms.mergesort)


def test_countsort_char():
    algorithm_test(algorithms.countsort_char)
