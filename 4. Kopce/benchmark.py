from random import sample, seed
from timeit import timeit

from numpy.lib.polynomial import poly1d
from heap import Heap
from matplotlib import pyplot as plt
from numpy import polyfit, array
from math import log2
from typing import Dict, List, Tuple

SEED = "trees"
START = 1
END = 300_001
REPEAT = 1

MIN_N = 10_000
STEP_N = 10_000
MAX_N = 100_000

GRAPH_DIR = "graph/"
PLOT_DIR = "plots/"


def time_insert(heap: Heap, lst: list):
    return timeit(lambda: [heap.insert(el) for el in lst], number=REPEAT)


def time_extract_max(heap: Heap):
    return timeit(lambda: [heap.extract_max() for _ in range(len(heap))], number=REPEAT)


def plot_benchmark(benchmarks: List[Tuple[Dict[int, float], str]]):
    for benchmark, label in benchmarks:
        x = array(list(benchmark.keys()))
        y = array(list(benchmark.values()))
        x_linlog = array([key * log2(key) for key in benchmark.keys()])

        series, = plt.plot(x, y, "o", label=label)
        coefficients = polyfit(x_linlog, y, 1)
        fit = poly1d(coefficients)
        plt.plot(x, fit(x_linlog), color=series._color, linestyle="--",
                 label=label + " nlog(n) fit")

    plt.legend()


if __name__ == "__main__":
    seed(SEED)
    sample_list = sample(range(START, END), MAX_N)

    heap2 = {n: Heap(2) for n in range(MIN_N, MAX_N + STEP_N, STEP_N)}
    heap3 = {n: Heap(3) for n in range(MIN_N, MAX_N + STEP_N, STEP_N)}
    heap4 = {n: Heap(4) for n in range(MIN_N, MAX_N + STEP_N, STEP_N)}

    t_insert_heap2 = {n: time_insert(heap, sample_list[:n])
                      for n, heap in heap2.items()}
    t_insert_heap3 = {n: time_insert(heap, sample_list[:n])
                      for n, heap in heap3.items()}
    t_insert_heap4 = {n: time_insert(heap, sample_list[:n])
                      for n, heap in heap4.items()}
    plt.title("Insertion")
    plt.ylabel("time to build heap [s]")
    plt.xlabel("number of elements to build heap from []")
    plot_benchmark([(t_insert_heap2, "2-ary"),
                    (t_insert_heap3, "3-ary"),
                    (t_insert_heap4, "4-ary")])
    plt.savefig(PLOT_DIR + "insert.jpg")
    plt.close()
    with open(f"{GRAPH_DIR}heap2.html", "w") as f:
        heap2[MIN_N].to_html(f)
    with open(f"{GRAPH_DIR}heap4.html", "w") as f:
        heap4[MIN_N].to_html(f)
    with open(f"{GRAPH_DIR}heap2.xml", "w") as f:
        heap2[MIN_N].to_xml(f)
    with open(f"{GRAPH_DIR}heap4.xml", "w") as f:
        heap4[MIN_N].to_xml(f)

    t_extract_max_heap2 = {n: time_extract_max(heap)
                           for n, heap in heap2.items()}
    t_extract_max_heap3 = {n: time_extract_max(heap)
                           for n, heap in heap3.items()}
    t_extract_max_heap4 = {n: time_extract_max(heap)
                           for n, heap in heap4.items()}
    plt.title("Extract max")
    plt.ylabel("time to extract all max elements in heap [s]")
    plt.xlabel("number of elements in heap []")
    plot_benchmark([(t_extract_max_heap2, "2-ary"),
                    (t_extract_max_heap3, "3-ary"),
                    (t_extract_max_heap4, "4-ary")])
    plt.savefig(PLOT_DIR + "extract_max.jpg")
    plt.close()

    with open(f"{GRAPH_DIR}heap2-extracted.html", "w") as f:
        heap2[MIN_N].to_html(f)
    with open(f"{GRAPH_DIR}heap4-extracted.html", "w") as f:
        heap4[MIN_N].to_html(f)
    with open(f"{GRAPH_DIR}heap2-extracted.xml", "w") as f:
        heap2[MIN_N].to_xml(f)
    with open(f"{GRAPH_DIR}heap4-extracted.xml", "w") as f:
        heap4[MIN_N].to_xml(f)
