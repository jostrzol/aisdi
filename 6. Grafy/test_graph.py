import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname)

from graph import Graph


def test_init_graph():
    graph = Graph()
    assert graph._graph == [[[0, 0, 1], [0, 0, 1]]]
    assert graph._height == 1
    assert graph._width == 2
    assert graph._start == (0, 0)
    assert graph._finish == (1, 0)


def test_graph_1():
    graph = Graph([[0, 2, 3],
                   [4, 5, 6],
                   [7, 0, 9]])

    assert graph._height == 3
    assert graph._width == 3


def test_graph_2():
    graph = Graph([[0, 2],
                   [3, 4],
                   [5, 6],
                   [7, 0]])

    assert graph._height == 4
    assert graph._width == 2


def test_graph_3():
    graph = Graph([[1, 0, 3, 4],
                   [5, 6, 0, 8]])

    assert graph._height == 2
    assert graph._width == 4
