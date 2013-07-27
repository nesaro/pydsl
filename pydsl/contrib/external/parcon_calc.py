from parcon import number, Forward, InfixExpr
import operator
expr = Forward()
term = number[float] | "(" + expr + ")"
term = InfixExpr(term, [("*", operator.mul), ("/", operator.truediv)])
term = InfixExpr(term, [("+", operator.add), ("-", operator.sub)])

expr << term(name="expr")

print expr.parse_string("1+2") # prints 3
print expr.parse_string("1+2+3") # prints 6
print expr.parse_string("1+2+3+4") # prints 10
print expr.parse_string("3*4") # prints 12
print expr.parse_string("5+3*4") # prints 17
print expr.parse_string("(5+3)*4") # prints 32
print expr.parse_string("10/4") # prints 2.5
