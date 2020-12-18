import math

class NodeType:
    # Represents a specific type of node, either an operator (e.g. multiply, add, etc.) or an integer
    # precedence is used for order of operation
    def __init__(self, value, precedence=None, run=None, allow_swaps=True, is_operator=True):
        self.value = value
        self.precedence = precedence
        self.run = run
        self.allow_swaps = allow_swaps
        self.is_operator = is_operator

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.__repr__()


def make_number_type(number):
    return NodeType(number, precedence=8, is_operator=False, run=lambda p, _, __: p)


operators = {
    "*": NodeType("*", precedence=3, run=lambda _, l, r: l * r),
    "+": NodeType("+", precedence=2, run=lambda _, l, r: l + r),
    "(": NodeType("(", allow_swaps=False),
    ")": NodeType(")"),
    "-": NodeType("-", precedence=2, run=lambda _, l, r: l - r),
    "/": NodeType("/", precedence=3, run=lambda _, l, r: l / r),
    "sin": NodeType("sin", allow_swaps=False, run=lambda _, __, r: math.sin(r))
}


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
        left = id(self.left) if self.left else ""
        right = id(self.right) if self.right else ""
        parent = id(self.parent) if self.parent else ""
        return f"V: {self.type.value} id: {id(self)} R: {right} L: {left} P: {parent}"

    def has_parent(self):
        return self.parent is not None


def get_node_type(value):
    if value in operators:
        return operators[value]
    if type(value) is int:
        return make_number_type(value)
    else:
        raise NotImplementedError(f"Operation '{value}' unimplemented")


def swap_with_parent(node):
    parent = node.parent
    grandparent = parent.parent
    if grandparent:
        if grandparent.left == parent:
            grandparent.left = node
        elif grandparent.right == parent:
            grandparent.right = node
        else:
            raise RuntimeError("Node's grandparent doesn't have parent as child")
    if node == parent.left:
        parent.left, parent.right, node.left, node.right = node.left, node.right, parent, parent.right
    elif node == parent.right:
        parent.left, parent.right, node.left, node.right = node.left, node.right, parent.left, parent
    else:
        raise RuntimeError("Node's parent doesn't have it as a child.")


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


def make_tree(nodes):
    root = Node(operators["("])
    active = root

    for node in nodes:
        if node.type.value == ")":
            opening_node = active.parent
            while opening_node.type.value != "(":
                opening_node = opening_node.parent
                if opening_node is None:
                    # print(active)
                    raise NotImplementedError("couldn't find matching bracket")
            pop_node(opening_node)
            active = opening_node.parent
        else:
            while active \
                    and active.type.allow_swaps \
                    and node.type.allow_swaps and active.type.precedence >= node.type.precedence:
                active = active.parent
            insert_node(active, node)
            active = node
        # print(active)
        # pretty_print_tree(root)

    return root.right  # since we don't want to include the bracket


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


def make_node_from_string(value):
    if value in operators:
        return Node(operators[value])
    else:
        return Node(make_number_type(float(value)))


def is_multi_character_node(character, previous_node):
    return character not in operators or (character == "-" and (previous_node is None or previous_node.type.is_operator))


def should_skip(c):
    return c == " "


# Converts a mathematical string into an ordered list of nodes that could then be connected together to form a tree.
def parse(expr):
    nodes = []
    in_progress_node = []
    for character in expr.strip():
        # First deal with any in_progress nodes
        if in_progress_node:
            # If numeric we keep building the current node.
            if character not in operators and not should_skip(character):
                in_progress_node.append(character)
                continue
            # Otherwise the current node is done and we append it to the list
            else:
                nodes.append(make_node_from_string("".join(in_progress_node)))
                in_progress_node = []  # Reset in_progress_node
        if should_skip(character):  # Skip whitespace
            continue
        elif is_multi_character_node(character, nodes[-1] if nodes else None):
            in_progress_node.append(character)
        else:
            nodes.append(make_node_from_string(character))

    # Finish the current node if any
    if in_progress_node:
        nodes.append(make_node_from_string("".join(in_progress_node)))

    return nodes


def validate(nodes):
    unclosed_brackets = 0
    for node in nodes:
        if node.type.value == "(":
            unclosed_brackets += 1
        if node.type.value == ")":
            unclosed_brackets -= 1
            if unclosed_brackets < 0:
                raise Exception("Too many closing brackets.")
    if unclosed_brackets != 0:
        raise Exception("Too many opening brackets")


def evaluate_node(node):
    if node is None:
        return None
    return node.type.run(node.type.value, evaluate_node(node.left), evaluate_node(node.right))


def compute(equation):
    nodes = parse(equation)
    validate(nodes)
    root = make_tree(nodes)
    return evaluate_node(root)
