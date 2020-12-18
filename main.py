from compute import compute

if __name__ == '__main__':
    while True:
        try:
            expression = input("Input an expression: \n")
            print("Answer: " + str(compute(expression)))
        except Exception as e:
            print("An error occurred: " + str(e))
        print()

