#!/usr/bin/env python
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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

from pydsl.Grammar.Definition import Grammar
import logging
LOG=logging.getLogger(__name__)

class Alphabet(object):
    """Defines a set of valid elements"""
    @property
    def minsize(self):
        return 1 #FIXME: In some cases could be 0

    @property
    def maxsize(self):
        return 1

class GrammarCollection(Alphabet, tuple):
    """Uses a list of grammar definitions"""
    def __init__(self, grammarlist):
        Alphabet.__init__(self)
        for x in self:
            if not isinstance(x, Grammar):
                raise TypeError("Expected Grammar, Got %s:%s" % (x.__class__.__name__,x))

    def __str__(self):
        return str([str(x) for x in self])

    def __add__(self, other):
        return GrammarCollection(tuple.__add__(self,other))

class Encoding(Alphabet):
    """Defines an alphabet using an encoding string"""
    def __init__(self, encoding):
        Alphabet.__init__(self)
        self.encoding = encoding

    def __hash__(self):
        return hash(self.encoding)

    def __eq__(self, other):
        try:
            return self.encoding == other.encoding
        except AttributeError:
            return False

    def __getitem__(self, item):
        from pydsl.Grammar import String
        try:
            return String(chr(item))
        except (ValueError, TypeError):
            raise KeyError

    def __contains__(self, item):
        try:
            self[item]
        except KeyError:
            return False
        else:
            return True

    def __str__(self):
        return self.encoding

    def enum(self):
        if self.encoding == "ascii":
            limit = 128
        elif self.encoding == "unicode":
            limit = 9635
        from pydsl.Grammar import String
        return [String(chr(x)) for x in range(limit)]
