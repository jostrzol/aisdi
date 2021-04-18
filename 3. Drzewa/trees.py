from __future__ import annotations
from typing import Optional, Tuple
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
                    self.left = BST_node(data, parent=self)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = BST_node(data, parent=self)
                else:
                    self.right.insert(data)
        else:
            self.data = data

# Delete Node
    def delete(self, data):
        if data < self.data:
            if self.left:
                self.left = self.left.delete(data)
                if self.left is not None:
                    self.left.parent = self
            return self
        if data > self.data:
            if self.right:
                self.right = self.right.delete(data)
                if self.right is not None:
                    self.right.parent = self
            return self
        if self.right is None:
            return self.left
        if self.left is None:
            return self.right
        min_larger_node = self.right.min_node()
        min_larger_node.parent = min_larger_node.parent.delete(
            min_larger_node.data)
        self.data = min_larger_node.data
        return self

# Search Node
    def search(self, data):
        if self.data == data:
            return self

        if self.data < data:
            if self.right is not None:
                return self.right.search(data)
            else:
                return None

        if self.right is not None:
            return self.left.search(data)
        else:
            return None

# Node with minimum value
    def min_node(self):
        current = self
        while current.left is not None:
            current = current.left
        return current

# Node with maximum value
    def max_node(self):
        current = self
        while current.right is not None:
            current = current.right
        return current

# Left -> Root -> Right
    def InOrderTraversal(self) -> list:
        res = []
        if self.left:
            res = self.left.InOrderTraversal()
        res.append(self.data)
        if self.right:
            res = res + self.right.InOrderTraversal()
        return res

# Left -> Right -> Root
    def PostOrderTraversal(self) -> list:
        res = []
        if self.left:
            res += self.left.PostOrderTraversal()
        if self.right:
            res += self.right.PostOrderTraversal()
        res.append(self.data)
        return res

# Root -> Left -> Right
    def PreOrderTraversal(self) -> list:
        res = [self.data]
        if self.left:
            res += self.left.PreOrderTraversal()
        if self.right:
            res += self.right.PreOrderTraversal()
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

# Insert Node
    def insert(self, data):
        self._root.insert(data)
        if self._root.parent is not None:
            self._root = self._root.parent

# Delete Node
    def delete(self, data):
        self._root = self._root.delete(data)
        if self._root is None:
            self._root = BST_node(None)
        self._root.parent = None

# Search Node
    def search(self, data):
        return self._root.search(data)

# Node with minimum value
    def min_node(self):
        return self._root.min_node()

# Node with maximum value
    def max_node(self):
        return self._root.max_node()

# Left -> Root -> Right
    def InOrderTraversal(self) -> list:
        return self._root.InOrderTraversal()

# Left -> Right -> Root
    def PostOrderTraversal(self) -> list:
        return self._root.PostOrderTraversal()

# Root -> Left -> Right
    def PreOrderTraversal(self) -> list:
        return self._root.PreOrderTraversal()

    def to_html(self, f: TextIOWrapper):
        html_head = ('<!DOCTYPE html> <html lang="en" class="">  <head> '
                     '<meta charset="UTF-8"> 	<link rel="stylesheet" href='
                     '"tree.css"> </head>')
        f.write(html_head)
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
        # if parent is not None:
        #     self.height = self.parent.height
        # else:
        #     self.height = 0

    def _fix_balance_insert(self):
        """
        fix balance of an unbalanced (self._balance == 2 or -2) node,
        which happened during insertion
        returns the node which ends up in self position after fixing
        """
        if abs(self._balance) <= 1:
            return self

        if self._balance < 0:
            child = self.left
        else:
            child = self.right

        if child._balance < 0:
            grandchild = child.left
        else:
            grandchild = child.right

        if self._balance * child._balance < 0:
            # grandchild is between child and self, need two roations
            grandchild._rotate()
            grandchild._rotate()

            growth_point = self._balance * grandchild._balance

            if growth_point == 0:
                # grandchild._balance must have been 0,
                # so now everything is balanced
                self._balance = 0
                child._balance = 0
            elif growth_point > 0:
                # grown tree is now in the "inner side" of child,
                # so self must be unbalanced to the "inner side"
                # and child is balanced;
                # inner side is left if child._balance == -1
                # and right if child._balance == 1

                self._balance = child._balance
                child._balance = 0
            else:
                # grown tree is now in the "inner side" of self,
                # so child must be unbalanced to the "inner side"
                # and self is balanced;
                # inner side is left if self._balance//2 == -1
                # and right if self._balance//2 == 1

                child._balance = self._balance//2
                self._balance = 0

            # either way grandchild is on top and is balanced
            grandchild._balance = 0

            return grandchild  # grandchild comes on top
        else:
            # child is between granchild and self,
            # need one roation
            child._rotate()
            self._balance = 0
            child._balance = 0
            return child  # child comes on top

    def _propagate_balance_insert(self, change):

        self._balance += change
        self = self._fix_balance_insert()

        if self.parent is not None and self._balance != 0:
            if self is self.parent.left:
                change = -1
            else:
                change = 1

            self.parent._propagate_balance_insert(change)
        else:
            return self

    def _rotate(self):
        """
        rotate self around self.parent
        """
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
                    self._propagate_balance_insert(-1)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = AVL_node(data, parent=self)
                    self._propagate_balance_insert(1)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    def _fix_balance_delete(self) -> Tuple[AVL_node, bool]:
        """
        fix balance od a node after shortening of one of its children
        returns the node which ends up in self position after fixing
        and wether the height of the tree shortened
        """
        if abs(self._balance) <= 1:
            return self, self._balance == 0

        if self._balance < 0:
            child = self.left  # right was shortened
        else:
            child = self.right  # left was shortened

        if child._balance < 0:
            grandchild = child.left
        else:
            grandchild = child.right

        if self._balance * child._balance < 0:
            # grandchild is between child and self, need two roations
            grandchild._rotate()
            grandchild._rotate()

            balance_point = self._balance * grandchild._balance

            if balance_point == 0:
                # grandchild._balance must have been 0,
                # so now everything is balanced
                self._balance = 0
                child._balance = 0
            elif balance_point > 0:
                # "outer" child of grandchild is bigger than "inner" one
                # the rest is same as smaller of the two

                self._balance = -grandchild._balance
                child._balance = 0
            else:
                # "inner" child of grandchild is bigger than "outer" one
                # the rest is same as smaller of the two

                child._balance = -grandchild._balance
                self._balance = 0

            # either way grandchild is on top and is balanced
            grandchild._balance = 0

            return grandchild, True  # grandchild comes on top
        else:
            # child is between granchild and self,
            # need one roation
            child._rotate()

            balance_point = self._balance * child._balance

            if balance_point > 0:
                # the "outer" child of child is bigger than the "inner" one

                self._balance = 0
                child._balance = 0
                return child, True  # child comes on top
            else:
                # the "inner" and "outer" children of child are equally big

                child._balance = -self._balance//2
                self._balance = self._balance//2
                return child, False  # child comes on top

    def _propagate_balance_delete(self, change):

        self._balance -= change
        self, changed = self._fix_balance_delete()

        if self.parent is not None and changed:
            if self is self.parent.left:
                change = -1
            else:
                change = 1

            self.parent._propagate_balance_delete(change)

    def delete(self, data):
        if data < self.data:
            if self.left:
                new_left, should_replace = self.left.delete(data)
                if should_replace:
                    self.left = new_left
                    if self.left is not None:
                        self.left.parent = self
                    self._propagate_balance_delete(-1)
                return None, False
        if data > self.data:
            if self.right:
                new_right, should_replace = self.right.delete(data)
                if should_replace:
                    self.right = new_right
                    if self.right is not None:
                        self.right.parent = self
                    self._propagate_balance_delete(1)
                return None, False

        if self.right is None:
            return self.left, True
        if self.left is None:
            return self.right, True
        min_larger_node = self.right.min_node()
        min_larger_node.parent, _ = min_larger_node.parent.delete(
            min_larger_node.data)
        self.data = min_larger_node.data
        return None, False

    def to_html(self, f: TextIOWrapper):
        f.write(f"<a>{self.data}/{self._balance}</a>\n")
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


class AVL(BST):
    def __init__(self, data=None):
        self._root = AVL_node(data)

    def delete(self, data):
        new_root, should_replace = self._root.delete(data)
        if should_replace:
            self._root = new_root
            if self._root is None:
                self._root = AVL_node(None)
            self._root.parent = None
        if self._root.parent is not None:
            self._root = self._root.parent


class NoParentError(Exception):
    def __init__(self, node: AVL_node):
        super().__init__('The given node does not have a parent')
        self.node: AVL_node = node


# quick test
if __name__ == "__main__":
    seed('trees')

    a = AVL()
    lst = sample(range(3000), 1000)
    for el in lst:
        a.insert(el)
    with open('AVL.html', 'w') as f:
        a.to_html(f)
    with open('AVL.xml', 'w') as f:
        a.to_xml(f)
    for i, el in enumerate(lst[len(lst)//4:len(lst)*3//4]):
        a.delete(el)
        # with open(f'{i}|AVL-{el}.html', 'w') as f:
        #     a.to_html(f)

    with open('AVL-deleted.html', 'w') as f:
        a.to_html(f)
    with open('AVL-deleted.xml', 'w') as f:
        a.to_xml(f)

    # b2 = BST(2)
    # b2.insert(3)
    # a2 = AVL(2)
    # a2.insert(3)

    # b2.delete(2)
    # b2.delete(3)
    # b2.insert(6)
    # a2.delete(2)
    # a2.delete(3)
    # a2.insert(6)
    # pass

    # b1 = AVL(27)
    # b1.insert(14)
    # b1.insert(35)
    # b1.insert(10)
    # b1.insert(19)
    # b1.insert(31)
    # b1.insert(42)
    # print(b1.InOrderTraversal())
    # b1.delete(35)
    # b1.delete(36)
    # print(b1.min_node().data)
    # print(b1.search(19))
    # print(b1.search(20))
    # print(b1.InOrderTraversal())

    # b1.delete(27)
    # print(b1.InOrderTraversal())
