from compute import compute, operators


def print_supported_operators():
    supported_operators = sorted(operators.values(), key=lambda op: op.precedence if op.precedence else -1)
    print("Supported Operators:", end=" ")

    for supported_operator in supported_operators:
        print(supported_operator, end=" ")
    print()


if __name__ == '__main__':
    print_supported_operators()
    while True:
        try:
            expression = input("Input an expression: \n")
            print("Answer: " + str(compute(expression)))
        except Exception as e:
            print("An error occurred: " + str(e))
        print()
