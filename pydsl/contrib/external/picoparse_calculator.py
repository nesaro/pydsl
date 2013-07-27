#!/usr/bin/env python
# Copyright (c) 2009, Andrew Brehaut, Steven Ashley
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, 
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, 
#   this list of conditions and the following disclaimer in the documentation  
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.

"""calculator.py - an example of infix expression parsing.

This example shows a simple approach to parsing a recursive infix expression 
using picoparse. It supports the four basic arithmetic operators, integer and 
floating point numbers, negatives, precedence order parenthesis.

The first half of the program defines a small set of syntax tree classes that
will be created by the various parsers. These nodes also know how to evaluate 
themselves.

The second half describes the parser itself. `expression` is the top level 
parser, and is described last as a specialisation of `choice` over binary 
operations and terms.

This parser assumes that whenever a bin_op is encountered, the left item is a 
term, and the right is another complex expression. Operator precedence is 
worked out by asking the node to `merge` with its right hand node. Examine
`bin_op` and `BinaryNode.merge` to see how this works.
"""

from string import digits as digit_chars

from picoparse import compose, p as partial
from picoparse import one_of, many1, choice, tri, commit, optional, fail, follow
from picoparse.text import run_text_parser, lexeme, build_string, whitespace, newline, as_string

# syntax tree classes
operators = ['-','+','*','/']
operator_functions = {
    '-': lambda l, r: l - r,
    '+': lambda l, r: l + r,
    '*': lambda l, r: l * r,
    '/': lambda l, r: l / r,
}
    

class ValueNode(object):
    """This is a leaf node for single numeric values. 
    
    Evaluates to itself, has maximum precedence
    """
    def __init__(self, value):
        self.left = value
        self.precedence = 1000

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.left)
        
    def evaluate(self):
        return self.left


class ParentheticalNode(object):
    """This node encapsulates a child node. 
    
    This node will be merged into BinaryNodes as if it were a single 
    value; This protects parenthesized trees from having order adjusted.   
    """
    def __init__(self, child):
        self.child = child
        self.precedence = 1000
    
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.child)
    
    def evaluate(self):
        return self.child.evaluate()
        
        
class BinaryNode(object):
    def __init__(self, left, op):
        self.left = left
        self.op = op
        self.right = None
        self.precedence = operators.index(op)
    
    def merge(self, right):
        if self.precedence >= right.precedence:
            self.right = right.left
            right.left = self
            return right
        else:
            self.right = right
            return self

    def __repr__(self):
        return "%s(%r, %r, %r)" % (self.__class__.__name__, self.left, 
                                                            self.op, 
                                                            self.right)
        
    def evaluate(self):
        return operator_functions[self.op](self.left.evaluate(), 
                                           self.right.evaluate())


# parser
digits = partial(lexeme, as_string(partial(many1, partial(one_of, digit_chars))))
operator = partial(lexeme, partial(one_of, operators))
    
@tri
def bin_op():
    left = term()
    op = operator()
    commit()
    right = expression()
    whitespace()
    
    n = BinaryNode(left, op)
    return n.merge(right) 
    
@tri
def parenthetical():
    whitespace()
    one_of('(')
    commit()
    whitespace()
    v = expression()
    whitespace()
    one_of(')')
    whitespace()
    return ParentheticalNode(v)

def int_value():
    return int(digits())

@tri
def float_value():
    whole_part = digits()
    one_of('.')
    commit()
    decimal_part = digits()
    return float('%s.%s' % (whole_part, decimal_part))

def value():
    is_negative = optional(partial(one_of, '-'), False)
    val = choice(float_value, int_value) * (is_negative and -1 or 1)
    return ValueNode(val)

term = partial('term', choice, parenthetical, partial('value', lexeme, value))
    
expression = partial('expression', choice, bin_op, term)

run_calculator = partial(run_text_parser, expression)

def calc(exp):
    tree, _ = run_calculator(exp)
    print exp, '=', tree.evaluate()
    print tree
    print

if __name__ == "__main__":
    exp = True
    while exp:
        exp = raw_input('> ')
        calc(exp)

    