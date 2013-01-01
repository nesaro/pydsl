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
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)


def terminal_symbol_reducer(symbol, word, production):
    """ Reduces a terminal symbol """
    from pydsl.Grammar.Tree import ParseTree
    if not isinstance(word, str):
        word = str(word)
    validresults = []
    if symbol.boundariesrules.policy == "min":
        LOG.debug("terminal_symbol_reducer: policy: min")
        for begin in range(0, len(word)):
            for end in range(begin, len(word)+1):
                if symbol.check(word[begin:end]):
                    LOG.debug("terminal_symbol_reducer: parsed:"+ str(word[begin:end]))
                    validresults.append(ParseTree(begin, end, [symbol], word[begin:end], production))
                    break #found the smallest valid symbol at begin
    elif symbol.boundariesrules.policy == "max":
        LOG.debug("terminal_symbol_reducer: policy: max")
        for begin in range(0, len(word)):
            maxword = 0
            for end in range(begin, len(word)+1):
                if symbol.check(word[begin:end]):
                    LOG.debug("terminal_symbol_reducer: parsed:"+ str(word[begin:end]))
                    maxword = end
            if maxword > 0:
                validresults.append(ParseTree(begin, maxword, [symbol], word[begin:maxword], production))
    elif symbol.boundariesrules.policy == "fixed":
        LOG.debug("terminal_symbol_reducer: policy: fixed")
        size = symbol.boundariesrules.size
        for begin in range(0, len(word)):
            if symbol.check(word[begin:begin + size]):
                LOG.debug("__auxReducer: parsed:"+ str(word[begin:begin + size]))
                validresults.append(ParseTree(begin, begin + size, [symbol], word[begin:begin + size], production))
    else:
        raise Exception("terminal_symbol_reducer: Unknown size policy")
    return validresults

def terminal_symbol_consume(symbol, word):
    """ Reduces a terminal symbol. Always start from left"""
    from pydsl.Grammar.Tree import ParseTree
    begin = 0
    if symbol.boundariesrules.policy == "min":
        for end in range(begin, len(word)+1):
            if symbol.check(word[begin:end]):
                return [ParseTree(begin, end, [symbol], word[begin:end], symbol)]
    elif symbol.boundariesrules.policy == "max":
        LOG.debug("terminal_symbol_consume: policy: max")
        maxword = 0
        for end in range(begin, len(word)+1):
            if symbol.check(word[begin:end]):
                LOG.debug("terminal_symbol_reducer: parsed:"+ str(word[begin:end]))
                maxword = end
        if maxword > 0:
           return[ParseTree(begin, maxword, [symbol], word[begin:maxword],
               symbol)]
    elif symbol.boundariesrules.policy == "fixed":
        size = symbol.boundariesrules.size
        LOG.debug("terminal_symbol_consume: policy: fixed " + str(size))
        if len(word) >= size and symbol.check(word[:size]):
            return [ParseTree(0, size, [symbol], word[:size], symbol)]
    else:
        raise Exception("terminal_symbol_consume: Unknown size policy")
    return []

def locate_result_borders(results):
    """ Finds the most conservative borders values"""
    leftborder = 0
    rightborder = 10**10
    for result in results:
        leftpos = result.leftpos
        rightpos = result.rightpos
        if leftpos is None and rightpos is None:
            return (rightborder, leftborder)
        if leftpos > leftborder:
            leftborder = leftpos
        if rightpos < rightborder:
            rightborder = rightpos
    return leftborder, rightborder

class Parser(object):
    """Parser abstract class. At this time, all parsers are tree based"""
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
    def __init__(self, bnfgrammar, packagedependencies = None):
        from pydsl.Alphabet.Lexer import BNFLexer
        self._lexer = BNFLexer(bnfgrammar)
        terminalsymbollist = bnfgrammar.getTerminalSymbols()
        for ts in terminalsymbollist:
            from pydsl.Grammar.Symbol import WordTerminalSymbol
            if isinstance(ts, WordTerminalSymbol):
                LOG.critical("BottomUp parsers can't handle WordTerminalSymbol yet")
                raise Exception
        Parser.__init__(self, bnfgrammar)
        
