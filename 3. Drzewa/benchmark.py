from random import sample, seed
from timeit import timeit
from trees import BST, AVL
from matplotlib import pyplot as plt
from numpy import polyfit, array
from typing import Dict

SEED = "trees"
START = 1
END = 300001
REPEAT = 1

MIN_N = 1000
STEP_N = 5000
MAX_N = 100000


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

    avl_x = array(list(benchmark_avl.keys()))
    avl_y = array(list(benchmark_avl.values()))

    bst_plt, =  plt.plot(list(benchmark_bst.keys()), list(
        benchmark_bst.values()), "bo", label="BST")
    bst_a, bst_b = polyfit(bst_x, bst_y, 1)
    plt.plot(bst_x, (bst_a * bst_x), "b")

    avl_plt, = plt.plot(list(benchmark_avl.keys()), list(
        benchmark_avl.values()), "ro", label="AVL")
    avl_a, avl_b = polyfit(avl_x, avl_y, 1)
    plt.plot(avl_x, (avl_a * avl_x), "r")

    plt.legend(handles=[bst_plt, avl_plt])


if __name__ == "__main__":
    seed(SEED)
    sample_list = sample(range(START, END), MAX_N)

    bsts = {n: BST() for n in range(MIN_N, MAX_N + STEP_N, STEP_N)}
    avls = {n: AVL() for n in range(MIN_N, MAX_N + STEP_N, STEP_N)}

    t_insert_bst = {n: time_insert(tree, sample_list[:n])
                    for n, tree in bsts.items()}
    t_insert_avl = {n: time_insert(tree, sample_list[:n])
                    for n, tree in avls.items()}
    plt.ylabel("time to build tree [s]")
    plt.xlabel("number of elements to build tree from []")
    plot_benchmark(t_insert_bst, t_insert_avl)
    plt.savefig("plots/insert.jpg")
    plt.close()
    with open("BST.html", "w") as f:
        bsts[1000].to_html(f)
    with open("AVL.html", "w") as f:
        avls[1000].to_html(f)

    t_search_bst = {n: time_search(tree, sample_list[:n])
                    for n, tree in bsts.items()}
    t_search_avl = {n: time_search(tree, sample_list[:n])
                    for n, tree in avls.items()}
    plt.ylabel("time to search for elements in tree [s]")
    plt.xlabel("number of elements to search for in tree []")
    plot_benchmark(t_search_bst, t_search_avl)
    plt.savefig("plots/search.jpg")
    plt.close()

    t_delete_bst = {n: time_delete(tree, sample_list[:n])
                    for n, tree in bsts.items()}
    t_delete_avl = {n: time_delete(tree, sample_list[:n])
                    for n, tree in avls.items()}
    plt.ylabel("time to delete elements in tree [s]")
    plt.xlabel("number of elements to delete in tree []")
    plot_benchmark(t_delete_bst, t_delete_avl)
    plt.savefig("plots/delete.jpg")
    plt.close()
    with open("BST-deleted.html", "w") as f:
        bsts[1000].to_html(f)
    with open("AVL-deleted.html", "w") as f:
        avls[1000].to_html(f)
