# Algorithm inspired heavily from explanations at https://www.rhyscitlema.com/algorithms/expression-parsing-algorithm/

import math

from util import *


class NodeType:
    """
    Represents a specific type of node, either an operator (e.g. multiply, add, etc.) or a value (pi, 3.4, etc.)
    @param value : the operator symbol or the value
    @:param run: A function to evaluate the operator
    @:param allow_swaps: used for open brackets to specify that the order in the tree is fixed
    @:param is_constant: used to signal to a following minus that it's either a minus or a negative (i.e. 5*-5 vs 5-5)
    @:param right_associative: true for operands such as ^ since order of operation is a^(b^c) not (a^b)^c
    @:param is_function: if a function isn't followed by a bracket it will add brackets
    """

    def __init__(self, value, is_function, precedence, run, allows_swaps=lambda _: True,
                 right_associative=False):
        self.value = value
        self.precedence = precedence
        self.run = run
        self.allows_swaps = allows_swaps
        self.right_associative = right_associative
        self.is_function = is_function

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return self.__repr__()


class Constant(NodeType):
    def __init__(self, value):
        super().__init__(value, precedence=float("inf"), is_function=False, run=lambda _, __: value)


class Operator(NodeType):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs, is_function=False)


class Function(NodeType):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs, is_function=True, precedence=float("inf"))


# Special case to differ between a negative (after an operator) or a minus (after a constant)
def minus_should_allow_swap(active_node):
    return type(active_node) == Constant if active_node is not None else True


operators = {
    "*": Operator("*", precedence=3, run=lambda l, r: l * r),
    "+": Operator("+", precedence=2, run=lambda l, r: l + r if l is not None else r),
    "(": Operator("(", precedence=float("inf"), allows_swaps=lambda _: False, run=None),
    ")": Operator(")", precedence=None, run=None),
    "-": Operator("-", precedence=2, allows_swaps=minus_should_allow_swap,
                  run=lambda l, r: l - r if l is not None else -r),
    "/": Operator("/", precedence=3, run=lambda l, r: l / r),
    "sin": Function("sin", run=lambda _, r: math.sin(r)),
    "cos": Function("cos", run=lambda _, r: math.cos(r)),
    "tan": Function("tan", run=lambda _, r: math.tan(r)),
    "pi": Constant(math.pi),
    "e": Constant(math.e),
    "^": Operator("^", precedence=4, right_associative=True, run=lambda l, r: l ** r),
    "!": Operator("!", precedence=5, run=lambda l, __: math.factorial(l))
}


def make_tree(nodes):
    def should_move_active_up(active, new):
        if not active:
            return False
        if not active.type.allows_swaps(None):
            return False
        if new.type.right_associative:
            return active.type.precedence > new.type.precedence
        else:
            return active.type.precedence >= new.type.precedence

    root = make_node_from_string("(")
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
            if node.type.allows_swaps(active.type):
                while should_move_active_up(active, node):
                    active = active.parent
            insert_node(active, node)
            active = node
        # print(active)
        # pretty_print_tree(root)

    return root.right  # since we don't want to include the bracket


def make_node_from_string(value):
    if value in operators:
        return Node(operators[value])
    else:
        return Node(Constant(float(value)))


# Converts a mathematical string into an ordered list of nodes that could then be connected together to form a tree.
def parse(expr):
    nodes = []
    in_progress_node = []
    for character in expr.strip():
        # First deal with any in_progress nodes
        if in_progress_node:
            # If numeric we keep building the current node.
            if character not in operators and not character == " ":
                in_progress_node.append(character)
                continue
            # Otherwise the current node is done and we append it to the list
            else:
                nodes.append(make_node_from_string("".join(in_progress_node)))
                in_progress_node = []  # Reset in_progress_node
        node = nodes[-1] if nodes else None
        if character == " ":  # Skip whitespace
            continue
        elif character not in operators:
            in_progress_node.append(character)
        else:
            nodes.append(make_node_from_string(character))

    # Finish the current node if any
    if in_progress_node:
        nodes.append(make_node_from_string("".join(in_progress_node)))

    # Add brackets around e.g. sin functions
    i = 0
    while i < len(nodes) - 1:
        if nodes[i].type.is_function and nodes[i + 1].type.value != "(":
            if type(nodes[i + 1].type) != Constant:
                raise Exception("Missing parentheses around function")
            nodes.insert(i + 1, make_node_from_string("("))
            nodes.insert(i + 3, make_node_from_string(")"))
        i += 1

    return nodes


def validate_input(nodes):
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
    return node.type.run(evaluate_node(node.left), evaluate_node(node.right))


def compute(expression):
    try:
        nodes = parse(expression)
        validate_input(nodes)
        root = make_tree(nodes)
        result = round(evaluate_node(root), 15)
        if int(result) == result:
            result = int(result)
        return result
    except Exception as e:
        print("Failed to computed expression: " + expression)
        raise e


if __name__ == '__main__':
    test_expr = "sin (+3)"
    print(compute(test_expr))