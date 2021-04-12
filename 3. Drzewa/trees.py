class BST:

    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data

# Insert Node
    def insert(self, data):

        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = BST(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = BST(data)
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
    def InOrderTraversal(self, root):
        res = []
        if root:
            res = self.InOrderTraversal(root.left)
            res.append(root.data)
            res = res + self.InOrderTraversal(root.right)
        return res


# quick test
root = BST(27)
root.insert(14)
root.insert(35)
root.insert(10)
root.insert(19)
root.insert(31)
root.insert(42)
print(root.InOrderTraversal(root))
