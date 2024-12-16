import unittest
import lark
from lark import Lark, Transformer, v_args

# Import the original calculator implementation
from calc import calc_grammar, CalculateTree

class CalculatorErrorHandlingTests(unittest.TestCase):
    def setUp(self):
        # Create a parser with the original grammar and transformer
        self.calc_parser = Lark(calc_grammar, parser='lalr', transformer=CalculateTree())

    def test_valid_expressions(self):
        """Test basic valid expressions work correctly"""
        test_cases = [
            ("1 + 2", 3.0),
            ("a = 5", 5.0),
            ("b = 3 * 2", 6.0),
            ("a + b", 11.0),
            ("-5", -5.0),
            ("(1 + 2) * 3", 9.0)
        ]
        
        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                result = self.calc_parser.parse(expr)
                self.assertAlmostEqual(result, expected)

    def test_undefined_variable(self):
        """Test handling of undefined variables"""
        with self.assertRaises(Exception) as context:
            self.calc_parser.parse("x + 5")
        
        self.assertTrue("Variable not found" in str(context.exception))

    def test_division_by_zero(self):
        """Test division by zero behavior"""
        with self.assertRaises(ZeroDivisionError):
            self.calc_parser.parse("10 / 0")

    def test_syntax_errors(self):
        """Test various syntax error scenarios"""
        syntax_error_cases = [
            "1 ++2",  # Double operator
            "1 + ",   # Incomplete expression
            "+ 5",    # Leading operator
            "1 + * 2" # Consecutive operators
        ]
        
        for expr in syntax_error_cases:
            with self.subTest(expr=expr):
                with self.assertRaises(lark.exceptions.LarkError):
                    self.calc_parser.parse(expr)

    def test_complex_error_scenarios(self):
        """Test more complex error scenarios"""
        error_cases = [
            "a = b + 1",  # Undefined variable in assignment
            "(1 + 2",     # Unbalanced parentheses
            "1 2 + 3"     # Invalid token sequence
        ]
        
        for expr in error_cases:
            with self.subTest(expr=expr):
                with self.assertRaises((lark.exceptions.LarkError, Exception)):
                    self.calc_parser.parse(expr)

    def test_nested_errors(self):
        """Test error handling in nested expressions"""
        nested_error_cases = [
            "((1 + ",      # Nested incomplete expression
            "((x + 5) * z" # Undefined variables in nested expression
        ]
        
        for expr in nested_error_cases:
            with self.subTest(expr=expr):
                with self.assertRaises((lark.exceptions.LarkError, Exception)):
                    self.calc_parser.parse(expr)

def main():
    unittest.main()

if __name__ == '__main__':
    main()