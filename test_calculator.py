"""Unit tests for the Smart Calculator expression evaluator."""

import math
import unittest

import calculator


class EvaluateTests(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(calculator.evaluate("2+3*4"), 14.0)
        self.assertEqual(calculator.evaluate("(2+3)*4"), 20.0)
        self.assertEqual(calculator.evaluate("10-3-2"), 5.0)

    def test_percent(self):
        self.assertEqual(calculator.evaluate("50%"), 0.5)
        self.assertEqual(calculator.evaluate("(2+3)%"), 0.05)

    def test_functions(self):
        self.assertAlmostEqual(calculator.evaluate("sin(30)"), 0.5)
        self.assertEqual(calculator.evaluate("sqrt(16)"), 4.0)
        self.assertEqual(calculator.evaluate("ln(1)"), 0.0)
        self.assertEqual(calculator.evaluate("log(100)"), 2.0)

    def test_division_by_zero(self):
        with self.assertRaises(calculator.CalcError) as ctx:
            calculator.evaluate("1/0")
        self.assertEqual(ctx.exception.code, "zero")

    def test_invalid_function(self):
        with self.assertRaises(calculator.CalcError) as ctx:
            calculator.evaluate("foo(1)")
        self.assertEqual(ctx.exception.code, "func")

    def test_invalid_character(self):
        with self.assertRaises(calculator.CalcError) as ctx:
            calculator.evaluate("2$3")
        self.assertEqual(ctx.exception.code, "char")

    def test_domain_errors_are_calc_errors(self):
        for expression in ("sqrt(-1)", "log(0)", "ln(-1)"):
            with self.subTest(expression=expression):
                with self.assertRaises(calculator.CalcError) as ctx:
                    calculator.evaluate(expression)
                self.assertEqual(ctx.exception.code, "expr")


class FormatNumberTests(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(calculator.format_number(5.0), "5")

    def test_fraction(self):
        self.assertEqual(calculator.format_number(0.5), "0.5")

    def test_special_values(self):
        self.assertEqual(calculator.format_number(math.nan), "Error")
        self.assertEqual(calculator.format_number(math.inf), "Error")


if __name__ == "__main__":
    unittest.main()
