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
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

"""

Parser expression grammars

Loosely based on pymeta

https://launchpad.net/pymeta

See also http://en.wikipedia.org/wiki/Parsing_expression_grammar

"""

from .Definition import Grammar, String
from pydsl.Alphabet import Alphabet

class ZeroOrMore(Grammar):
    def __init__(self, element):
        Grammar.__init__(self)
        self.element = element

    def first(self):
        return Choice([self.element])


class OneOrMore(Grammar):
    def __init__(self, element):
        Grammar.__init__(self)
        self.element = element

    def first(self):
        return Choice([self.element])

class Sequence(Grammar, list):
    def __init__(self, *args, **kwargs):
        base_alphabet = kwargs.pop('base_alphabet', None)
        Grammar.__init__(self, base_alphabet)
        list.__init__(self, *args, **kwargs)
        for x in self:
            if not isinstance(x, Grammar):
                raise TypeError(x)

    def __hash__(self):
        return hash(tuple(self))

    @classmethod
    def from_string(cls, string):
        return cls([String(x) for x in string])

class Choice(Alphabet, Grammar):
    """Uses a list of grammar definitions with common base alphabets"""
    def __init__(self, grammarlist):
        Alphabet.__init__(self, grammarlist)
        base_alphabet_list = []
        for x in self:
            if not isinstance(x, Grammar):
                raise TypeError("Expected Grammar, Got %s:%s" % (x.__class__.__name__,x))
            if x.alphabet not in base_alphabet_list:
                base_alphabet_list.append(x.alphabet)
        if len(base_alphabet_list) != 1:
            raise ValueError('Different base alphabets from members %s' % base_alphabet_list)
        Grammar.__init__(self, base_alphabet_list[0])

    def __str__(self):
        return str([str(x) for x in self])

    def __add__(self, other):
        return Choice(GrammarCollection.__add__(self,other))

class Optional(object):
    def __init__(self, element):
        Grammar.__init__(self)
        self.element = element

class Not(object):
    def __init__(self, element):
        self.element = element

class And(object):
    def __init__(self, element):
        Grammar.__init__(self)
        self.element = element

