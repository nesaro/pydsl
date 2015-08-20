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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2015, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pydsl.grammar.definition import Grammar
from pydsl.check import check

class Symbol(object):
    pass

class NonTerminalSymbol(str, Symbol):
    def __init__(self, name):
        Symbol.__init__(self)

    def __str__(self):
        return "<NonTS: " + self + ">"

    def __hash__(self):
        return str.__hash__(self)

    def __eq__(self, other):
        if not isinstance(other, NonTerminalSymbol):
            return False
        return str.__eq__(self,other)


class TerminalSymbol(Symbol):

    def __init__(self, gd):
        if not isinstance(gd, Grammar):
            raise TypeError("Expected Grammar, got %s" % (gd,))
        Symbol.__init__(self)
        if not gd:
            raise Exception
        self.gd = gd

    def __hash__(self):
        return hash(self.gd)

    def check(self, data):# ->bool:
        """Checks if input is recognized as this symbol"""
        return check(self.gd, data)

    def first(self):
        return self.gd.first

    def __eq__(self, other):
        """StringTerminalSymbol are equals if definition and names are equal"""
        try:
            return self.gd == other.gd
        except AttributeError:
            return False

    def __str__(self):
        return "<TS: " + str(self.gd) + ">"

class NullSymbol(Symbol):
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(NullSymbol, cls).__new__(cls)
        return cls._instance

    def __eq__(self, other):
        return isinstance(other, NullSymbol)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        return False

class EndSymbol(Symbol):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EndSymbol, cls).__new__(cls)
        return cls._instance

    def __hash__(self):
        assert(EndSymbol._instance is not None)
        return hash(id(self._instance))

    def __eq__(self, other):
        result = isinstance(other, EndSymbol) or EndSymbol == other
        return result

    def __bool__(self):
        return False

    def __str__(self):
        return "$"
