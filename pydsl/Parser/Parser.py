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
from pydsl.Lex import lexer_factory
from pydsl.Config import load

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)


def terminal_symbol_reducer(symbol, data, fixed_start = False):
    """ Reduces a terminal symbol """
    from pydsl.Extract import extract
    from pydsl.Tree import ParseTree
    validresults = extract(symbol.gd, data, fixed_start)
    validresults = sorted(validresults, key=lambda x:x[1]-x[0])
    if symbol.boundariesrules == "min":
        validresults = validresults[:1]
    elif symbol.boundariesrules == "max":
        validresults = validresults[-1:]
    elif symbol.boundariesrules == "any":
        pass
    elif isinstance(symbol.boundariesrules , int):
        pass
    else:
        raise ValueError("Unknown boundaries rules")
    return [ParseTree(begin, end, symbol, data[begin:end]) for (begin, end, _) in validresults]

class Parser(object):
    """Expands an input based on grammar rules
    At this time, all parsers are tree based"""
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
        self._productionset = bnfgrammar

class BottomUpParser(Parser):
    """ leaf to root parser"""
    def __init__(self, bnfgrammar):
        self._lexer = lexer_factory(bnfgrammar.alphabet())
        self._productionset = bnfgrammar


def parser_factory(grammar, parser = None):
    if isinstance(grammar, str):
        grammar = load(grammar)
    from pydsl.Grammar.BNF import BNFGrammar
    if isinstance(grammar, BNFGrammar):
        if parser == "descent":
            from pydsl.Parser.Backtracing import BacktracingErrorRecursiveDescentParser
            return BacktracingErrorRecursiveDescentParser(grammar)
        elif parser in ("auto" , "default" , "weighted", None):
            #TODO Guess best parser
            from pydsl.Parser.Weighted import WeightedParser
            return WeightedParser(grammar)
        else:
            raise Exception("Wrong parser name: " + str(parser))
    else:
        raise ValueError(grammar)


def parse(definition, data, parser = "auto"):
    return parser_factory(definition, parser)(data)
