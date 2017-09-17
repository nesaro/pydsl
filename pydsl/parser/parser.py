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
from pydsl.lex import lexer_factory

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)


class Parser(object):
    """Expands an input based on grammar rules
    At this time, all parsers are tree based"""
    def __init__(self, productionset):
        self._productionset = productionset
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
    def _reduce_terminal(self, symbol, data, showerrors = False):
        from pydsl.check import check
        from pydsl.tree import ParseTree
        result = check(symbol.gd, data)
        if result:
            return [ParseTree(0,1, symbol , data)]
        if showerrors and not result:
            return [ParseTree(0,1, symbol , data, valid = False)]
        return []

class BottomUpParser(Parser):
    """ leaf to root parser"""
    def __init__(self, bnfgrammar):
        self._lexer = lexer_factory(bnfgrammar.alphabet)
        super().__init__(bnfgrammar)


def parser_factory(grammar, parser = None):
    from pydsl.grammar.BNF import BNFGrammar
    if isinstance(grammar, BNFGrammar):
        if parser in ("auto" , "default" , "descent", None):
            from pydsl.parser.backtracing import BacktracingErrorRecursiveDescentParser
            return BacktracingErrorRecursiveDescentParser(grammar)
        elif parser == "lr0":
            from pydsl.parser.LR0 import LR0Parser
            return LR0Parser(grammar)
        elif parser == "ll1":
            from pydsl.parser.LL import LL1RecursiveDescentParser
            return LL1RecursiveDescentParser(grammar)
        else:
            raise Exception("Wrong parser name: " + str(parser))
    else:
        raise ValueError(grammar)


def parse(definition, data, parser = "auto"):
    return parser_factory(definition, parser)(data)
