#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is part of pydsl.
#
# pydsl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# pydsl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

"""Production rules"""

from pydsl.grammar.symbol import Symbol, TerminalSymbol, NullSymbol, EndSymbol
from pydsl.grammar.definition import Grammar
from pydsl.grammar.PEG import Choice

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

def list_eq(list1, list2):
    return len(list1) == len(list2) and all(list1[x] == list2[x] for x in range(len(list1)))

class Production(object):

    def __init__(self, leftside, rightside):
        # Left side must have at least one non terminal symbol
        for element in rightside:
            if not isinstance(element, Symbol):
                raise TypeError
        self.leftside = tuple(leftside)
        self.rightside = tuple(rightside)

    def __str__(self):
        """Pretty print"""
        leftstr = " ".join([x for x in self.leftside])
        rightstr = " ".join([str(x) for x in self.rightside])
        return leftstr + "::=" + rightstr

    def __eq__(self, other):
        try:
            if len(self.leftside) != len(other.leftside):
                return False
            if len(self.rightside) != len(other.rightside):
                return False
            if not list_eq(self.leftside, other.leftside):
                return False
            if not list_eq(self.rightside, other.rightside):
                return False
        except AttributeError:
            return False
        return True

    def __hash__(self):
        return hash(self.leftside) & hash(self.rightside)


#Only stores a ruleset, and methods to ask properties or validity check
class BNFGrammar(Grammar):

    def __init__(self, initialsymbol, fulllist, options=None):
        Grammar.__init__(self)
        self._initialsymbol = initialsymbol
        for rule in fulllist:
            if fulllist.count(rule) > 1:
                raise ValueError("Duplicated rule: " + str(rule))
        self.fulllist = tuple(fulllist)
        self.options = options or {}

    def __hash__(self):
        return hash(self.fulllist)

    @property
    def alphabet(self):
        return frozenset([x.gd for x in self.terminal_symbols])

    @property
    def productions(self):
        return [x for x in self.fulllist if isinstance(x, Production)]

    @property
    def terminal_symbols(self):
        return [x for x in self.fulllist if isinstance(x, TerminalSymbol)]

    def first(self):
        """Returns the a grammar definition that includes all first elements of this grammar"""
        return self.first_lookup(self.initialsymbol)

    def first_lookup(self, symbol, size=1):
        """
        Returns a Grammar Definition with the first n terminal symbols
        produced by the input symbol
        """
        if isinstance(symbol, (TerminalSymbol, NullSymbol)):
            return symbol.gd
        result = []
        for production in self.productions:
            if production.leftside[0] != symbol:
                continue
            for right_symbol in production.rightside:
                if right_symbol == symbol: #Avoids infinite recursion
                    break
                current_symbol_first = self.first_lookup(right_symbol, size)
                import collections
                from pydsl.grammar.definition import String
                if isinstance(current_symbol_first, collections.Iterable) and not isinstance(current_symbol_first, String):
                    result += current_symbol_first
                else:
                    result.append(current_symbol_first)
                if isinstance(current_symbol_first, String) or \
                        not isinstance(current_symbol_first, collections.Iterable) or \
                        (NullSymbol not in current_symbol_first):
                    break # This element doesn't have Null in its first set so there is no need to continue
        if not result:
            raise KeyError("Symbol doesn't exist in this grammar")
        return Choice(result)

    def next_lookup(self, symbol):
        """Returns the next TerminalSymbols produced by the input symbol within this grammar definition"""
        result = []
        if symbol == self.initialsymbol:
            result.append(EndSymbol())
        for production in self.productions:
            if symbol in production.rightside:
                nextindex = production.rightside.index(symbol) + 1
                while nextindex < len(production.rightside):
                    nextsymbol = production.rightside[nextindex]
                    firstlist = self.first_lookup(nextsymbol)
                    cleanfirstlist = Choice([x for x in firstlist if x != NullSymbol()])
                    result.append(cleanfirstlist)
                    if NullSymbol() not in firstlist:
                        break
                else:
                    result += self.next_lookup(production.leftside[0]) #reached the end of the rightside
        return result

    def __eq__(self, other):
        try:
            return self._initialsymbol == other.initialsymbol and list_eq(self.productions, other.productions)
        except AttributeError:
            return False

    @property
    def initialsymbol(self):
        return self._initialsymbol

    @property
    def main_production(self):
        """Returns main rule"""
        for rule in self.productions:
            if rule.leftside[0] == self._initialsymbol:
                return rule
        raise IndexError

    def getProductionsBySide(self, symbol):
        result = [rule for rule in self.productions if len(rule.leftside) == 1 and rule.leftside[0] == symbol]
        if not result:
            raise IndexError("Symbol: %s" % str(symbol))
        return result

    def getSymbols(self):
        """Returns every symbol"""
        symbollist = []
        for rule in self.productions:
            for symbol in rule.leftside + rule.rightside:
                if symbol not in symbollist:
                    symbollist.append(symbol)
        symbollist += self.terminal_symbols
        return symbollist

    def __str__(self):
        return str(list(map(str, self.productions)))
