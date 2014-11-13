# chemicalFormulas.py
#
# Copyright (c) 2003, 2007, Paul McGuire
#

from pyparsing import Word, Optional, OneOrMore, Group, ParseException

# define a simple Python dict of atomic weights, with chemical symbols
# for keys
atomicWeight = {
    "O"  : 15.9994,
    "H"  : 1.00794,
    "Na" : 22.9897,
    "Cl" : 35.4527,
    "C"  : 12.0107,
    "S"  : 32.0655,
    }

# define some strings to use later, when describing valid lists 
# of characters for chemical symbols and numbers
caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowers = caps.lower()
digits = "0123456789"

# Version 1
# Define grammar for a chemical formula
# - an element is a Word, beginning with one of the characters in caps,
#   followed by zero or more characters in lowers
# - an integer is a Word composed of digits
# - an elementRef is an element, optionally followed by an integer - if 
#   the integer is omitted, assume the value "1" as a default; these are 
#   enclosed in a Group to make it easier to walk the list of parsed 
#   chemical symbols, each with its associated number of atoms per 
#   molecule
# - a chemicalFormula is just one or more elementRef's
element = Word( caps, lowers )
integer = Word( digits )
elementRef = Group( element + Optional( integer, default="1" ) )
chemicalFormula = OneOrMore( elementRef )

# Version 2 - Auto-convert integers, and add results names
def convertIntegers(tokens):
    return int(tokens[0])
    
element = Word( caps, lowers )
integer = Word( digits ).setParseAction( convertIntegers )
elementRef = Group( element("symbol") + Optional( integer, default=1 )("qty") )
# pre-1.4.7, use this: 
# elementRef = Group( element.setResultsName("symbol") + Optional( integer, default=1 ).setResultsName("qty") )
chemicalFormula = OneOrMore( elementRef )


# Version 3 - Compute partial molecular weight per element, simplifying 
# summing
# No need to redefine grammar, just define parse action function, and
# attach to elementRef
def computeElementWeight(tokens):
    element = tokens[0]
    element["weight"] = atomicWeight[element.symbol] * element.qty
    
elementRef.setParseAction(computeElementWeight)

root_symbol = chemicalFormula

iclass = "pyparsing"
