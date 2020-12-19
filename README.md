# Math Expression Solver

As part of the Advent of Code competition, I wrote a custom parser and solver for math expressions.
The function  `compute.compute(expr)` takes in a string such as `"cos(-pi)"` and returns the result, `-1`.
Running `main.py` allows you to type in expressions and immediately see the results.

## Cool thing 1 (aka. the algorithm)

The solver goes through 3 steps.

1. Parse the string into a list of operands. For example `cos(-pi)` becomes
`["cos", "(", "-", "pi", ")"]`.

2. Make a binary tree representation of the expression.
This is the most "algorithmic intensive" part and is based on [this](https://www.rhyscitlema.com/algorithms/expression-parsing-algorithm/) algorithm from Rhyscitlema.

3. Solve the expression by recursively traversing the binary tree.

## Cool thing 2

All the operations (e.g. *, /, sin, cos) are specified in a list! This makes it really easy
to add new operations, or change the order of operations. Take a look at `operands`
in `compute.py`.