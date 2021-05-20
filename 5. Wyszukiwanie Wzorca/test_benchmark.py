from string_searching import find_n, find_kmp, find_kr
from typing import Callable, Dict, List
from matplotlib import pyplot as plt
import pytest
import json

ALGORITHMS = [find_n, find_kmp, find_kr]
SIZES = list(range(100, 1001, 100))
REPEAT = 1

TEXT_FILE = "reference/pan-tadeusz.txt"
OUT_FILE = "benchmark.json"

PLT_DIR = "plots/"

SEED = "text"


def alg_multiple(alg: Callable[[str, str], List[int]], text: str, strings: List[str]):
    for string in strings:
        alg(text, string)


@pytest.mark.parametrize("alg", ALGORITHMS)
@pytest.mark.parametrize("size", SIZES)
def test_benchmark(alg: Callable[[str, str], List[int]], size: int, benchmark):

    benchmark.extra_info["alg"] = alg.__name__
    benchmark.extra_info["size"] = size

    with open(TEXT_FILE) as f:
        text = f.read()

    strings = text.split()[:size]

    benchmark.pedantic(alg_multiple, (alg, text, strings), rounds=REPEAT)


if __name__ == "__main__":
    try:
        with open(OUT_FILE) as f:
            out = json.load(f)
    except FileNotFoundError:
        print(
            f"Run benchmark first using 'pytest --benchmark-json={OUT_FILE}'")
        exit(-1)

    pretty_names = {
        "find_n": "Naive",
        "find_kmp": "Knuth-Morris-Pratt",
        "find_kr": "Karp-Rabin",
    }

    benchmarks: Dict[str, Dict[int, float]] = {}
    for b in out['benchmarks']:
        alg = b['extra_info']['alg']
        size = b['extra_info']['size']
        time = b['stats']['mean']

        if alg in pretty_names:
            alg = pretty_names[alg]

        if alg not in benchmarks:
            benchmarks[alg] = {}

        benchmarks[alg][size] = time

    plt.title("Find")
    plt.xlabel("Number of words to find []")
    plt.ylabel("Time [s]")

    for name, b in benchmarks.items():
        x = b.keys()
        y = b.values()

        plt.plot(x, y, "-", label=name)

        plt.legend()

    plt.savefig(PLT_DIR + "find.jpg")
    plt.close()
