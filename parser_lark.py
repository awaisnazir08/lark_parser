from lark import Lark

# Define grammar for arithmetic expressions
grammar = """
    start: expr
    expr: term (("+"|"-") term)*
    term: factor (("*"|"/") factor)*
    factor: NUMBER | "(" expr ")"
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

# Create parser
parser = Lark(grammar, start='start', parser='lalr')

# Parse an expression
parse_tree = parser.parse("(3 + 5) * 2")
print(parse_tree.pretty())
