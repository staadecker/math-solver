class Node:
    # Represents a single node in the binary tree used to represent the mathematical expression.
    # self.type is an instance of NodeType and value is the string that
    def __init__(self, type, parent=None, left_child=None, right_child=None):
        self.type = type
        self.parent = parent
        self.left = left_child
        self.right = right_child

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        left = self.left.type.value if self.left else ""
        right = self.right.type.value if self.right else ""
        parent = self.parent.type.value if self.parent else ""
        return f"{self.type.value} R: {right} L: {left} P: {parent}"

    def has_parent(self):
        return self.parent is not None

def pop_node(node):
    if node.left is not None:
        raise RuntimeError("Can't pop")

    if node.parent:
        if node.parent.left == node:
            node.parent.left = node.right
        elif node.parent.right == node:
            node.parent.right = node.right
        else:
            raise RuntimeError("parent doesn't have current as child")

    node.right.parent = node.parent


def insert_node(parent, new):
    new.left = parent.right
    parent.right = new
    new.parent = parent


def pretty_print_tree(root):
    stack = [("", root)]
    print("Tree.")
    while stack:
        prefix, cur = stack.pop()

        if cur != root:
            print(prefix + "\u21B3" + " " * 5, end="")
        while True:
            print(cur.type.value, end="")

            if cur != root:
                prefix += " " if cur.parent.left else " "
                prefix += " " * (len(str(cur.type.value)) + 4)

            if cur.left:
                stack.append((prefix, cur.left))

            cur = cur.right
            if cur is None:
                print()
                break
            print(end=" --> ")
    print("End tree.")