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
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

from pydsl.Grammar.Definition import Grammar

class Alphabet(Grammar):
    """Defines a set of valid elements"""
    @property
    def first(self):
        return self

    @property
    def maxsize(self):
        return None

    @property
    def minsize(self):
        return 1 #FIXME: In some cases could be 0

class Choice(Alphabet, list):
    """Uses a list of grammar definitions"""
    def __init__(self, grammarlist, base_alphabet = None):
        Alphabet.__init__(self, base_alphabet)
        if not grammarlist:
            raise ValueError
        result = []
        from pydsl.Config import load
        for x in grammarlist:
            if isinstance(x, str):
                result.append(load(x))
            else:
                result.append(x)
        list.__init__(self, result)
        base_alphabet_list = []
        for x in self:
            if not isinstance(x, Grammar):
                raise TypeError("Expected Grammar, Got %s:%s" % (x.__class__.__name__,x))
            if x.base_alphabet not in base_alphabet_list:
                base_alphabet_list.append(x.base_alphabet)
        if len(base_alphabet_list) != 1:
            raise ValueError('Different base alphabets from members')

    def __add__(self, other):
        return Choice(list.__add__(self,other))

class Encoding(Alphabet):
    """Defines an alphabet using an encoding string"""
    def __init__(self, encoding):
        Alphabet.__init__(self)
        self.encoding = encoding

    def __eq__(self, other):
        try:
            return self.encoding == other.encoding
        except AttributeError:
            return False

    def __getitem__(self, item):
        from pydsl.Check import EncodingChecker
        if EncodingChecker(self).check(item):
            from pydsl.Grammar.Definition import String
            return String(item)
        raise KeyError

    @property
    def to_list(self):
        #FIXME: Only ascii
        from pydsl.Grammar.Definition import String
        return [String(chr(x)) for x in range(128)]
