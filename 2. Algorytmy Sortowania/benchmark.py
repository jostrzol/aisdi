from typing import Callable, Dict
from timeit import timeit
from matplotlib import pyplot as plt

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
