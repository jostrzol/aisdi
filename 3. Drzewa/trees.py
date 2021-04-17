from __future__ import annotations
from typing import Optional
from random import sample, seed
from io import TextIOWrapper


class BST_node:

    def __init__(self, data, parent: Optional[BST_node] = None):

        self.left: Optional[BST_node] = None
        self.right: Optional[BST_node] = None
        self.data = data

        self.parent = parent

# Insert Node
    def insert(self, data):

        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = BST_node(data, parent=self.left)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = BST_node(data, parent=self.right)
                else:
                    self.right.insert(data)
        else:
            self.data = data

# Print the Tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.data),
        if self.right:
            self.right.PrintTree()

# Left -> Root -> Right
    def InOrderTraversal(self) -> list:
        res = []
        if self.left:
            res = self.left.InOrderTraversal()
        res.append(self.data)
        if self.right:
            res = res + self.right.InOrderTraversal()
        return res

    def to_html(self, f: TextIOWrapper):
        f.write(f"<a>{self.data}</a>\n")
        if self.left is None and self.right is None:
            return
        f.write("<ul>\n")
        if self.left is not None:
            f.write("<li>\n")
            self.left.to_html(f)
            f.write("</li>\n")
        if self.right is not None:
            f.write("<li>\n")
            self.right.to_html(f)
            f.write("</li>\n")
        f.write("</ul>\n")

    def to_xml(self, f: TextIOWrapper):
        f.write(f"<data>{self.data}</data>\n")
        if self.left is not None:
            f.write("<left>\n")
            self.left.to_xml(f)
            f.write("</left>\n")
        if self.right is not None:
            f.write("<right>\n")
            self.right.to_xml(f)
            f.write("</right>\n")


class BST():
    def __init__(self, data=None):
        self._root = BST_node(data)

    def insert(self, data):
        self._root.insert(data)
        if self._root.parent is not None:
            self._root = self._root.parent

    def InOrderTraversal(self) -> list:
        return self._root.InOrderTraversal()

    def to_html(self, f: TextIOWrapper):
        html_header = '<!DOCTYPE html> <html lang="en" class="">  <head> 	'
        html_header += '<meta charset="UTF-8"> 	<link rel="stylesheet" href='
        html_header += '"tree.css"> </head>'
        f.write(html_header)
        f.write('<body>\n')
        f.write('<div class="tree">\n')
        f.write('<div class="canvas">\n')
        f.write('<ul>\n')
        f.write('<li>\n')
        self._root.to_html(f)
        f.write('</li>\n')
        f.write('</ul>\n')
        f.write('</div>\n')
        f.write('</div>\n')
        f.write('</body>\n')

    def to_xml(self, f: TextIOWrapper):
        f.write('<tree>\n')
        self._root.to_xml(f)
        f.write('</tree>\n')


class AVL_node(BST_node):

    def __init__(self, data, parent: Optional[AVL_node] = None):
        super().__init__(data, parent=parent)
        self.parent: AVL_node
        self.left: AVL_node
        self.right: AVL_node
        self._balance = 0

    def _propagate_balance(self):
        parent = self.parent
        if parent is None:
            return

        grown_child = None
        if self._balance == -1:
            grown_child = self.left
        elif self._balance == 1:
            grown_child = self.right

        if self is parent.left:
            parent._balance -= 1
        else:
            parent._balance += 1

        if abs(parent._balance) > 1:
            if parent._balance * self._balance < 0:
                # unbalanced tree is between self and parent, need two roations
                grown_child._rotate()
                grown_child._rotate()

                growth_point = parent._balance * grown_child._balance

                if growth_point == 0:
                    # grown_child._balance must have been 0,
                    # so now everything is balanced
                    parent._balance = 0
                    self._balance = 0
                elif growth_point > 0:
                    # grown tree is now in the "inner side" of self,
                    # so parent must be unbalanced to the "inner side"
                    # and self is balanced;
                    # inner side is left if self._balance == -1
                    # and right if self._balance == 1

                    parent._balance = self._balance
                    self._balance = 0
                else:
                    # grown tree is now in the "inner side" of parent,
                    # so self must be unbalanced to the "inner side"
                    # and parent is balanced;
                    # inner side is left if parent._balance/2 == -1
                    # and right if parent._balance/2 == 1

                    self._balance = parent._balance/2
                    parent._balance = 0

                # either way grown_child is on top and is balanced
                grown_child._balance = 0

                parent = grown_child  # grown_child comes on top
            else:
                # self is between the unbalanced tree and parent,
                # need one roation
                self._rotate()
                parent._balance = 0
                self._balance = 0
                parent = self  # self comes on top

        if parent is not None and parent._balance != 0:
            parent._propagate_balance()

    def _rotate(self):
        if self.parent is None:
            raise NoParentError(self)
        parent = self.parent
        grandpa = parent.parent
        if grandpa is not None:
            if parent is grandpa.left:
                grandpa.left = self
            else:
                grandpa.right = self
        self.parent = grandpa
        parent.parent = self

        if self is parent.right:
            parent.right = self.left
            if self.left is not None:
                self.left.parent = parent
            self.left = parent
        else:
            parent.left = self.right
            if self.right is not None:
                self.right.parent = parent
            self.right = parent

    def insert(self, data):
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = AVL_node(data, parent=self)
                    self.left._propagate_balance()
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = AVL_node(data, parent=self)
                    self.right._propagate_balance()
                else:
                    self.right.insert(data)
        else:
            self.data = data


class AVL(BST):
    def __init__(self, data=None):
        self._root = AVL_node(data)


class NoParentError(Exception):
    def __init__(self, node: AVL_node):
        super().__init__('The given node does not have a parent')
        self.node: AVL_node = node


# quick test
if __name__ == "__main__":
    seed('trees')

    # a1 = AVL(27)
    # a1.insert(14)
    # a1.insert(35)
    # a1.insert(16)
    # a1.insert(15)
    # a1.insert(31)
    # a1.insert(42)
    # print(a1.InOrderTraversal())

    a = AVL()
    for i in sample(range(3000), 80):
        a.insert(i)

    print(a.InOrderTraversal())
    with open('AVL.html', 'w') as f:
        a.to_html(f)
    with open('AVL.xml', 'w') as f:
        a.to_xml(f)

    a2 = AVL(27)
    a2.insert(14)
    a2.insert(35)
    a2.insert(10)
    a2.insert(9)
    a2.insert(31)
    a2.insert(42)
    print(a2.InOrderTraversal())

    b1 = BST(27)
    b1.insert(14)
    b1.insert(35)
    b1.insert(10)
    b1.insert(19)
    b1.insert(31)
    b1.insert(42)
    print(b1.InOrderTraversal())
