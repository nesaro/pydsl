#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of pydsl.
#
#pydsl is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pydsl is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

"""Parser module"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)


def terminal_symbol_reducer(symbol, word, production, fixed_start = False):
    """ Reduces a terminal symbol """
    if fixed_start:
        max_begin = 1
    else:
        max_begin = len(word)
    validresults = []
    for begin in range(0, max_begin):
        for end in range(begin, len(word)+1):
            if symbol.check(word[begin:end]):
                validresults.append((end-begin, begin, end))
    validresults = sorted(validresults, key=lambda x:x[0])
    if symbol.boundariesrules == "min":
        validresults = validresults[:1]
    elif symbol.boundariesrules == "max":
        validresults = validresults[-1:]
    elif symbol.boundariesrules == "any":
        pass
    elif isinstance(symbol.boundariesrules , int):
        #validresults = [x for x in validresults if x[0] == symbol.boundariesrules]
        pass
    else:
        raise ValueError("Unknown boundaries rules")
    from pydsl.Grammar.Tree import ParseTree
    return [ParseTree(begin, end, [symbol], word[begin:end], production) for (size, begin, end) in validresults]

class Parser(object):
    """Expands an input based on grammar rules
    At this time, all parsers are tree based"""
    def __init__(self, bnfgrammar):
        self._productionset = bnfgrammar

    def get_trees(self, word): # -> list:
        """ returns a ParseTree list with all guesses """
        raise NotImplementedError

    def __call__(self, word):
        return self.get_trees(word)

    @property
    def productionset(self):
        """returns productionset"""
        return self._productionset

class TopDownParser(Parser):
    """Top down parser like descent parser"""
    def __init__(self, bnfgrammar):
        Parser.__init__(self, bnfgrammar)

class BottomUpParser(Parser):
    """ leaf to root parser"""
    def __init__(self, bnfgrammar):
        from pydsl.Memory.Loader import load_lexer
        self._lexer = load_lexer(bnfgrammar.alphabet())
        Parser.__init__(self, bnfgrammar)
