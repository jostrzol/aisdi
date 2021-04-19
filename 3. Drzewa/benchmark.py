from random import sample, seed
from timeit import timeit

from numpy.lib.polynomial import poly1d
from trees import BST, AVL
from matplotlib import pyplot as plt
from numpy import polyfit, array
from math import log2
from typing import Dict

SEED = "trees"
START = 1
END = 300001
REPEAT = 1

MIN_N = 1000
STEP_N = 5000
MAX_N = 100000

GRAPH_DIR = "graph/"


def time_insert(tree: BST, lst: list):
    return timeit(lambda: [tree.insert(el) for el in lst], number=REPEAT)


def time_search(tree: BST, lst: list):
    return timeit(lambda: [tree.search(el) for el in lst], number=REPEAT)


def time_delete(tree: BST, lst: list):
    return timeit(lambda: [tree.delete(el) for el in lst], number=REPEAT)


def plot_benchmark(benchmark_bst: Dict[int, float],
                   benchmark_avl: Dict[int, float]):
    bst_x = array(list(benchmark_bst.keys()))
    bst_y = array(list(benchmark_bst.values()))
    bst_x_linlog = array([key * log2(key) for key in benchmark_bst.keys()])

    avl_x = array(list(benchmark_avl.keys()))
    avl_y = array(list(benchmark_avl.values()))
    avl_x_linlog = array([key * log2(key) for key in benchmark_avl.keys()])

    plt.plot(bst_x, bst_y, "bo", label="BST")
    bst_coefficients = polyfit(bst_x_linlog, bst_y, 1)
    bst_fit = poly1d(bst_coefficients)
    plt.plot(bst_x, bst_fit(bst_x_linlog), "b--", label="BST nlog(n) fit")

    plt.plot(avl_x, avl_y, "ro", label="AVL")
    avl_coefficients = polyfit(avl_x_linlog, avl_y, 1)
    avl_fit = poly1d(avl_coefficients)
    plt.plot(avl_x, avl_fit(avl_x_linlog), "r--", label="AVL nlog(n) fit")

    plt.legend()


if __name__ == "__main__":
    seed(SEED)
    sample_list = sample(range(START, END), MAX_N)

    bsts = {n: BST() for n in range(MIN_N, MAX_N + STEP_N, STEP_N)}
    avls = {n: AVL() for n in range(MIN_N, MAX_N + STEP_N, STEP_N)}

    t_insert_bst = {n: time_insert(tree, sample_list[:n])
                    for n, tree in bsts.items()}
    t_insert_avl = {n: time_insert(tree, sample_list[:n])
                    for n, tree in avls.items()}
    plt.title("Insertion")
    plt.ylabel("time to build tree [s]")
    plt.xlabel("number of elements to build tree from []")
    plot_benchmark(t_insert_bst, t_insert_avl)
    plt.savefig("plots/insert.jpg")
    plt.close()
    with open(f"{GRAPH_DIR}BST.html", "w") as f:
        bsts[1000].to_html(f)
    with open(f"{GRAPH_DIR}AVL.html", "w") as f:
        avls[1000].to_html(f)
    with open(f"{GRAPH_DIR}BST.xml", "w") as f:
        bsts[1000].to_xml(f)
    with open(f"{GRAPH_DIR}AVL.xml", "w") as f:
        avls[1000].to_xml(f)

    t_search_bst = {n: time_search(tree, sample_list[:n])
                    for n, tree in bsts.items()}
    t_search_avl = {n: time_search(tree, sample_list[:n])
                    for n, tree in avls.items()}
    plt.title("Search")
    plt.ylabel("time to search for elements in tree [s]")
    plt.xlabel("number of elements to search for in tree []")
    plot_benchmark(t_search_bst, t_search_avl)
    plt.savefig("plots/search.jpg")
    plt.close()

    t_delete_bst = {n: time_delete(tree, sample_list[:n])
                    for n, tree in bsts.items()}
    t_delete_avl = {n: time_delete(tree, sample_list[:n])
                    for n, tree in avls.items()}
    plt.title("Deletion")
    plt.ylabel("time to delete elements in tree [s]")
    plt.xlabel("number of elements to delete in tree []")
    plot_benchmark(t_delete_bst, t_delete_avl)
    plt.savefig("plots/delete.jpg")
    plt.close()
    with open(f"{GRAPH_DIR}BST-deleted.html", "w") as f:
        bsts[1000].to_html(f)
    with open(f"{GRAPH_DIR}AVL-deleted.html", "w") as f:
        avls[1000].to_html(f)
    with open(f"{GRAPH_DIR}BST-deleted.xml", "w") as f:
        bsts[1000].to_xml(f)
    with open(f"{GRAPH_DIR}AVL-deleted.xml", "w") as f:
        avls[1000].to_xml(f)
