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
    def __init__(self, type, name, weight = None, boundariesrules = None):
        if type == "string":
            weight = weight or 99
            boundariesrules = len(name)
        elif type == "grammar":
            weight = weight or 49
        elif type == "token":
            weight = weight or 49
            boundariesrules = 1
        Symbol.__init__(self, weight)
        if boundariesrules not in ("min","max","any") and not isinstance(boundariesrules, int):
            raise TypeError
        self.type = type
        self.name = name
        self.boundariesrules = boundariesrules

    def __hash__(self):
        return hash(self.type) ^ hash(self.name) ^ hash(self.boundariesrules)

    def check(self, data):# ->bool:
        """Checks if input is recognized as this symbol"""
        if self.type == "string":
            return data == self.name
        elif self.type == "grammar":
            from pydsl.Memory.Loader import load_checker
            checker = load_checker(self.name)
            return checker.check(data)
        elif self.type == "token":
            alphabet, token = self.name.split(".")
            alphabet = load(alphabet)
            symboldefinition = alphabet[token]
            checker = load_checker(symboldefinition)
            return checker.check(data)
        else:
            raise Exception


    def __eq__(self, other):
        """StringTerminalSymbol are equals if definition and names are equal"""
        try:
            if isinstance(other, str) and self.type == "string":
                return self.name == other
            return self.name == other.name and self.type == other.type and self.boundariesrules == other.boundariesrules
        except AttributeError:
            return False

    def __str__(self):
        return "<TS: " + str(self.type) + str(self.name) + ">"

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
