from typing import Callable, Dict
from timeit import timeit
from matplotlib import pyplot as plt

import algorithms as alg

default_benchmark_filename = "reference/lorem_ipsum.txt"


def benchmark_sort(
        func: Callable[[list], list], filename=default_benchmark_filename,
        number: int = 1, start: int = 50, stop: int = 302, step: int = 50):
    result = {}
    for n in range(start, stop, step):
        buffer = []
        m = 0
        with open(filename, "r") as f:
            for line in f:
                line.rstrip("\n")
                buffer.append([char for char in line])
                m += 1
                if m >= n:
                    break
        t = timeit(lambda: [func(line) for line in buffer], number=number)
        result[n] = t/number
    return result


def plot_benchmark(benchmark: Dict[int, float], filename: str):
    plt.plot(list(benchmark.keys()), list(benchmark.values()), "bo")
    plt.savefig(filename)
    plt.close()


if __name__ == "__main__":
    plot_dir = "plots/"
    number = 10
    to_benchmark = {
        "quicksort.png": alg.quicksort,
        "mergesort.png": alg.mergesort,
        "bubblesort.png": alg.bubblesort,
        "countsort_char.png": alg.countsort_char}

    for filename, func in to_benchmark.items():
        b = benchmark_sort(func, number=number)
        plot_benchmark(b, plot_dir + filename)
