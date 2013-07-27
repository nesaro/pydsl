#!/bin/env python
#===============================================================================
# Copyright (c) 2007 Jason Evans <jasone@canonware.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#===============================================================================
#
# Usage: example1.py [-v] "<input>"
#                          ^^^^^^^
#                          <input> is a string of whitespace-separated tokens.
#
# This program is a small example of how to use the Parsing module.  There is a
# long tradition of examples that parse simple mathematical expressions.  Most
# such series of examples start with a hierarchy of non-terminals/productions
# in order to get operator precedence right, then move on to demonstrate the
# parser generator's built-in precedence disambiguation facilities.  This
# example skips the traditional first step and jumps right to using operator
# precedence specifications.
#
# The parser supports four mathematical operations on integers: +, -, *, and /.
# Multiplication and division take precedence over addition and subtraction, as
# is traditional.
#
# In order to minimize clutter, this file omits numerous details that are
# important for understanding, especially if you are not experienced with
# parser generators.  You can find such information in the Parsing module's
# docstring-based documentation, by entering the following via the Python
# prompt:
#
#   >>> import Parsing
#   >>> help(Parsing)
#
#===============================================================================

import sys
import Parsing

#===============================================================================
# Tokens/precedences.  See Parsing documentation to learn about the
# significance of left-associative precedence.

class PAddOp(Parsing.Precedence):
    "%left pAddOp"
class TokenPlus(Parsing.Token):
    "%token plus [pAddOp]"
class TokenMinus(Parsing.Token):
    "%token minus [pAddOp]"

class PMulOp(Parsing.Precedence):
    "%left pMulOp >pAddOp"
class TokenStar(Parsing.Token):
    "%token star [pMulOp]"
class TokenSlash(Parsing.Token):
    "%token slash [pMulOp]"

class TokenInt(Parsing.Token):
    "%token int"
    def __init__(self, parser, i):
	Parsing.Token.__init__(self, parser)
	self.val = i

#===============================================================================
# Nonterminals, with associated productions.  In traditional BNF, the following
# productions would look something like:
#
#   AddOp ::= plus
#           | minus.
#   MulOp ::= star
#           | slash.
#   Expr ::= int
#          | Expr AddOp Expr
#          | Expr MulOp Expr.
#   Result ::= Expr.

class AddOp(Parsing.Nonterm):
    "%nonterm"
    def reducePlus(self, plus):
	"%reduce plus"
	self.variant = "plus"

    def reduceMinus(self, minus):
	"%reduce minus"
	self.variant = "minus"

class MulOp(Parsing.Nonterm):
    "%nonterm"
    def reduceStar(self, star):
	"%reduce star"
	self.variant = "star"

    def reduceSlash(self, slash):
	"%reduce slash"
	self.variant = "slash"

class Expr(Parsing.Nonterm):
    "%nonterm"
    def reduceInt(self, i):
	"%reduce int"
	self.val = i.val

    def reduceAdd(self, exprA, AddOp, exprB):
	"%reduce Expr AddOp Expr [pAddOp]"
	if AddOp.variant == "plus":
	    self.val = exprA.val + exprB.val
	    print "%d <- %d + %d" % (self.val, exprA.val, exprB.val)
	elif AddOp.variant == "minus":
	    self.val = exprA.val - exprB.val
	    print "%d <- %d - %d" % (self.val, exprA.val, exprB.val)

    def reduceMul(self, exprA, MulOp, exprB):
	"%reduce Expr MulOp Expr [pMulOp]"
	if MulOp.variant == "star":
	    self.val = exprA.val * exprB.val
	    print "%d <- %d * %d" % (self.val, exprA.val, exprB.val)
	elif MulOp.variant == "slash":
	    self.val = exprA.val / exprB.val
	    print "%d <- %d / %d" % (self.val, exprA.val, exprB.val)

# This is the start symbol; there can be only one such class in the grammar.
class Result(Parsing.Nonterm):
    "%start"
    def reduce(self, Expr):
	"%reduce Expr"
	print "Result: %d" % Expr.val

#===============================================================================
# Parser.

# Parser subclasses the Lr parser driver.  Since the grammar is unambiguous, we
# have no need of the Glr driver's extra functionality, though there is nothing
# preventing us from using it.
#
# If you are curious how much more work the GLR driver has to do, simply change
# the superclass from Parsing.Lr to Parsing.Glr, then, run this program with
# verbosity enabled.
class Parser(Parsing.Lr):
    def __init__(self, spec):
	Parsing.Lr.__init__(self, spec)

    # Brain-dead scanner.  The scanner does not have to be a method of this
    # class, so for more complex parsers it is no problem to separate the
    # scanner into a separate module.
    def scan(self, input):
	syms = {"+": TokenPlus,
		"-": TokenMinus,
		"*": TokenStar,
		"/": TokenSlash
		}

	for word in input.split(" "):
	    if word in syms:
		token = syms[word](self)
	    else:
		# Try to convert to an integer.
		try:
		    i = int(word)
		except:
		    raise Parsing.SyntaxError("Unrecognized token: %s" % word)
		token = TokenInt(parser, i)
	    # Feed token to parser.
	    self.token(token)
	# Tell the parser that the end of input has been reached.
	self.eoi()

#===============================================================================
# Main code.

# Introspect this module to generate a parser.  Enable all the bells and
# whistles.
spec = Parsing.Spec(sys.modules[__name__],
		    pickleFile="example1.pickle",
		    skinny=False,
		    logFile="example1.log",
		    graphFile="example1.dot",
		    verbose=True)
# example1.log is a human-readable representation of the parser tables.
# Suppose that you are trying to figure out what the parser is doing for a
# particular input, in this case, "2 * * 3".  If you have parsing verbosity
# enabled, you will see something like this:
#
#   STACK: <e>
#          0  
#   INPUT: int
#      --> [shift 1]
#   STACK: <e> int
#          0   1  
#   INPUT: star
#      --> [reduce Expr ::= int. [none]]
#   STACK: <e> Expr
#          0   3   
#      --> [shift 5]
#   STACK: <e> Expr star
#          0   3    5   
#   INPUT: star
#   Traceback (most recent call last):
#     File "./example1.py", line 186, in <module>
#       parser.scan(args[0])
#     File "./example1.py", line 151, in scan
#       self.token(token)
#     File "/home/jasone/Desktop/Parsing.py", line 2273, in token
#       self._act(token, tokenSpec)
#     File "/home/jasone/Desktop/Parsing.py", line 2300, in _act
#       raise SyntaxError, ("Unexpected token: %r" % sym)
#   Parsing.SyntaxError: Unexpected token: star
#
# Notice that the parser was in state 5 when the syntax error occurred.  Here
# is the relevant state from example1.log:
#
#   ============================================================================
#   State 5:
#            MulOp ::= star *. [none]
#     Goto:
#     Action:
#                 int : reduce MulOp ::= star. [none]
#   ============================================================================
#
# In this state, the only token that the parser knows how to handle is the int
# token.  We fed it a star token.  Whoops.
#
# As an aside, if your grammar has unresolvable conflicts, you can look at the
# log file and look for actions prefaced by XXX to diagnose the problem.
#
# Feed example1.dot to graphviz's dotty/dot in order to view/create a graphical
# representation of the precedence relationships.  As ASCII art, it looks
# something like this:
#
#   _________________   _______________   _________________
#   | pMulOp (left) |   | none (fail) |   | split (split) |
#   -----------------   ---------------   -----------------
#           |
#           |
#   ________v________
#   | pAddOp (left) |
#   -----------------

# Create a parser that uses the parser tables encapsulated by spec.  In this
# program, we are only creating one parser instance, but it is possible for
# multiple parsers to use the same Spec simultaneously.
parser = Parser(spec)

# Read input as a string from the command line; treat a leading -v specially,
# if present.
args = sys.argv[1:]
if len(sys.argv) > 1 and sys.argv[1] == "-v":
    # Enable verbose parsing output.
    parser.verbose = True
    args.pop(0)

# Parse command line input.
if len(args) > 0:
    parser.scan(args[0])

#===============================================================================
