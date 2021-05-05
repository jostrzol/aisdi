from io import TextIOWrapper
from random import sample, seed

TEST_GRAPH_DIR = "test_graph/"


class Heap:
    def __init__(self, degree: int = 2):
        self._degree = degree
        self._list = []

    def _parent_i(self, i: int):
        if i >= len(self._list):
            raise IndexError
        if i == 0:
            return None
        parent = (i - 1) // self._degree
        return parent

    def _children_i(self, i: int):
        if i >= len(self._list):
            raise IndexError
        start = min(self._degree*i + 1, len(self._list))
        end = min(start + self._degree, len(self._list))
        return range(start, end)

    def _swap(self, i: int, j: int):
        tmp = self._list[j]
        self._list[j] = self._list[i]
        self._list[i] = tmp

    def insert(self, value):
        self._list.append(value)
        i = len(self._list) - 1
        parent = self._parent_i(i)
        while parent is not None:
            if self._list[parent] < self._list[i]:
                self._swap(i, parent)
            i = parent
            parent = self._parent_i(parent)

    def _heapify(self, i: int):
        children_i = self._children_i(i)
        while children_i:
            max_i = max(children_i, key=lambda j: self._list[j])
            if self._list[max_i] > self._list[i]:
                self._swap(max_i, i)
                children_i = self._children_i(max_i)
                i = max_i
            else:
                return

    def extract_max(self):
        if not self._list:
            raise IndexError
        result = self._list[0]
        last = self._list.pop()
        if self._list:
            self._list[0] = last
            self._heapify(0)
        return result

    def _node_to_xml(self, f: TextIOWrapper, i: int):
        f.write(f"<data>{self._list[i]}</data>\n")
        for j, child_i in enumerate(self._children_i(i)):
            f.write(f"<child-{j}>\n")
            self._node_to_xml(f, child_i)
            f.write(f"</child-{j}>\n")

    def to_xml(self, f: TextIOWrapper):
        f.write("<heap>\n")
        if self._list:
            self._node_to_xml(f, 0)
        f.write("</heap>\n")

    def _node_to_html(self, f: TextIOWrapper, i: int):
        f.write(f"<a>{self._list[i]}</a>\n")
        children_i = self._children_i(i)
        if not children_i:
            return
        f.write("<ul>\n")
        for child_i in children_i:
            f.write('<li>\n')
            self._node_to_html(f, child_i)
            f.write('</li>\n')
        f.write("</ul>\n")

    def to_html(self, f: TextIOWrapper):
        html_head = ('<!DOCTYPE html> <html lang="en" class=""> <head> '
                     '<meta charset="UTF-8"> <link rel="stylesheet" href='
                     '"tree.css"> </head>')
        f.write(html_head)
        f.write('<body>\n')
        f.write('<div class="tree">\n')
        f.write('<div class="canvas">\n')
        f.write('<ul>\n')
        f.write('<li>\n')
        if self._list:
            self._node_to_html(f, 0)
        f.write('</li>\n')
        f.write('</ul>\n')
        f.write('</div>\n')
        f.write('</div>\n')
        f.write('</body>\n')

    def __len__(self):
        return len(self._list)


if __name__ == "__main__":
    seed("heap")

    heap2 = Heap(2)
    data = sample(range(1_000), 100)
    for x in data:
        heap2.insert(x)
    with open(TEST_GRAPH_DIR + "heap2.xml", "w") as f:
        heap2.to_xml(f)
    with open(TEST_GRAPH_DIR + "heap2.html", "w") as f:
        heap2.to_html(f)

    heap2_sorted = [heap2.extract_max() for _ in range(len(heap2))]
    print(heap2_sorted)
    assert(heap2_sorted == sorted(data, key=lambda x: -x))

    heap3 = Heap(3)
    for x in data:
        heap3.insert(x)
    with open(TEST_GRAPH_DIR + "heap3.xml", "w") as f:
        heap3.to_xml(f)
    with open(TEST_GRAPH_DIR + "heap3.html", "w") as f:
        heap3.to_html(f)

    heap3_sorted = [heap3.extract_max() for _ in range(len(heap3))]
    print(heap3_sorted)
    assert(heap3_sorted == sorted(data, key=lambda x: -x))

    heap10 = Heap(10)
    data = sample(range(10_000), 1000)
    for x in data:
        heap10.insert(x)
    with open(TEST_GRAPH_DIR + "heap10.xml", "w") as f:
        heap10.to_xml(f)
    with open(TEST_GRAPH_DIR + "heap10.html", "w") as f:
        heap10.to_html(f)

    heap10_sorted = [heap10.extract_max() for _ in range(len(heap10))]
    assert(heap10_sorted == sorted(data, key=lambda x: -x))
