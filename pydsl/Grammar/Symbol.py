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

class Symbol(object):
    def __init__(self, name, weight): 
        self.name = name
        self._weight = weight

    def __eq__(self, other):
        if not isinstance(other, Symbol):
            return False
        return self.name == other.name

    def __ne__(self, other):
        """Operator != """
        return not self.__eq__(other)

    @property
    def weight(self):
        return self._weight

    def first(self, length = 1):
        """Returns the list of possible first elements"""
        raise NotImplementedError

class NonTerminalSymbol(Symbol):
    def __init__(self, name,  weight = 50):
        Symbol.__init__(self, name, weight)

    def __str__(self):
        return "<NonTS: " + self.name + ">"

    def __eq__(self, other):
        if not isinstance(other, NonTerminalSymbol):
            return False
        return self.name == other.name

class TerminalSymbol(Symbol): 
    def __init__(self, name, weight, boundariesrules): 
        Symbol.__init__(self, name, weight)
        if boundariesrules not in ("min","max","any") and not isinstance(boundariesrules, int):
            raise TypeError
        self.boundariesrules = boundariesrules

    def check(self, data):# ->bool:
        """Checks if input is recognized as this symbol"""
        raise NotImplementedError


class StringTerminalSymbol(TerminalSymbol): #FIXME This class is equivalent to a StaticGrammarDefinition
    def __init__(self, string):
        if len(string) < 1:
            raise TypeError
        TerminalSymbol.__init__(self, "StrSymbol " + string, 99, len(string))
        self.definition = string

    def check(self, tokenlist):# -> bool:
        return tokenlist == self.definition

    def __eq__(self, other):
        """StringTerminalSymbol are equals if definition and names are equal"""
        if isinstance(other, str):
            return self.definition == other
        if not isinstance(other, StringTerminalSymbol):
            return False
        if self.definition != other.definition:
            return False
        if self.name != other.name:
            return False
        return True

    def __len__(self):
        return len(self.definition)

    def first(self):
        return self.definition[0]

    def __str__(self):
        return "<StringTS: " + self.definition + ">"


class WordTerminalSymbol(TerminalSymbol):#boundariesrules: [max,min,fixedsize]
    def __init__(self, name, grammarname, boundariesrules):
        TerminalSymbol.__init__(self, name, 49, boundariesrules)
        self.grammarname = grammarname
        self.__checker =  None 

    @property
    def checker(self):
        if self.__checker is None:
            from pydsl.Memory.Loader import load_checker
            self.__checker = load_checker(self.grammarname)
        return self.__checker

    def __eq__(self, other):
        if not isinstance(other, WordTerminalSymbol):
            return False
        if self.grammarname != other.grammarname:
            return False
        if self.name != other.name:
            return False
        return True

    def check(self, string):
        result =  self.checker.check(string)
        return result

    def __str__(self):
        return "<WordTS: " + self.grammarname + ">"


class UnknownSymbol(TerminalSymbol):
    def __init__(self):
        TerminalSymbol.__init__(self, "Unknown", 1, "any")

    def __eq__(self, other):
        return isinstance(other, UnknownSymbol)

    def check(self, data):
        return bool(data)

class NullSymbol(Symbol):
    def __init__(self):
        Symbol.__init__(self, "Null", 100)

    def __eq__(self, other):
        return isinstance(other, NullSymbol)

    def bool(self):
        return False

class EndSymbol(TerminalSymbol):
    pass
