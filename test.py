import unittest
from compute import *

class ComputeTests(unittest.TestCase):
    def test_valid(self):
        cases = {
            # BASIC OPERATIONS
            "4*3": 12,
            "4+3": 7,
            "(3)": 3,
            "5-3": 2,
            "5-6": -1,
            "5*-6": -30,
            "-3": -3,
            "5/3": 1.666666666,
            "5.3": 5.3,
            "2.5 + 2.5 * 2": 7.5,
            "sin(0.523598775)": 0.5,
            "tan(1)": 1.557407725,
            "cos(1)": 0.540302305,
            "cos(pi)": -1,
            "cos pi": -1,
            "4^2": 16,
            "4^(1/2)": 2,
            "4^0.5": 2,
            "(3)-2": 1,
            "3!^2": 36,
            "5!+1": 121,
            # WHITE SPACE
            " 4 + 3 ": 7,
            # ORDER OF OPERATIONS
            "4+3*7": 25,
            "3*7+4": 25,
            "(3+4)*7/7": 7,
            "2 + ((1+1)*2)*2 ": 10,
            "2 + ((-1+1)*2)*2 ": 2,
            "1-1^2": 0,
            "-1^2": -1,
            "4^2^3": 65536,
            "6 / 3 * 2": 4,
            "cos(0)*2": 2,
            "sin (pi/2) * 2": 2,
            "-cos (-pi)": 1,

        }

        for expr, ans in cases.items():
            self.assertAlmostEqual(ans, compute(expr), 8, msg=f"Failed case: {expr}={ans}")

    # def test_invalid_brackets(self):
    #     cases = ["(3", "((4+5)"]
    #
    #     for expr in cases:
    #         self.assertRaises(NotImplementedError, compute(expr))


if __name__ == '__main__':
    unittest.main()
