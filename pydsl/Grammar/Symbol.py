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

"""Symbols"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pydsl.Grammar.Definition import StringGrammarDefinition, GrammarDefinition

class Symbol(object):
    def __init__(self, weight):
        self._weight = weight

    @property
    def weight(self):
        return self._weight

    def first(self, length = 1):
        """Returns the list of possible first elements"""
        raise NotImplementedError

class NonTerminalSymbol(Symbol):
    def __init__(self, name,  weight = 50):
        Symbol.__init__(self, weight)
        self.name = name

    def __str__(self):
        return "<NonTS: " + self.name + ">"

    def __eq__(self, other):
        if not isinstance(other, NonTerminalSymbol):
            return False
        return self.name == other.name

class TerminalSymbol(Symbol): 
    def __init__(self, gd, weight = None, boundariesrules = None):
        if isinstance(gd, StringGrammarDefinition):
            weight = weight or 99
            boundariesrules = len(gd.string)
        else:
            weight = weight or 49
        Symbol.__init__(self, weight)
        if boundariesrules not in ("min","max","any") and not isinstance(boundariesrules, int):
            raise TypeError
        self.gd = gd
        self.boundariesrules = boundariesrules

    def __hash__(self):
        return hash(self.gd) ^ hash(self.boundariesrules)

    def check(self, data):# ->bool:
        """Checks if input is recognized as this symbol"""
        from pydsl.Memory.Loader import load_checker
        checker = load_checker(self.gd)
        return checker.check(data)

    @property
    def first(self):
        return self.gd.first


    def __eq__(self, other):
        """StringTerminalSymbol are equals if definition and names are equal"""
        try:
            return self.gd == other.gd and self.boundariesrules == other.boundariesrules
        except AttributeError:
            return False

    def __str__(self):
        return "<TS: " + str(self.gd) + ">"

class UnknownSymbol(Symbol):
    def __init__(self):
        Symbol.__init__(self, 1)
        self.boundariesrules = "any"

    def __eq__(self, other):
        return isinstance(other, UnknownSymbol)

    def check(self, data):
        return bool(data)

class NullSymbol(Symbol):
    def __init__(self):
        Symbol.__init__(self, 100)

    def __eq__(self, other):
        return isinstance(other, NullSymbol)

    def __bool__(self):
        return False

class EndSymbol(TerminalSymbol):
    pass
