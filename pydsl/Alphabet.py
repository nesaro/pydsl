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
    def to_list(self):
        """Returns a list of allowed grammars"""
        raise NotImplementedError

    def __contains__(self, token):
        """Returns true if the alphabet contains the token"""
        raise NotImplementedError

    @property
    def minsize(self):
        return 1 #FIXME: In some cases could be 0

class AlphabetListDefinition(Alphabet):
    """Uses a list of grammar definitions"""
    def __init__(self, grammarlist):
        if not grammarlist:
            raise ValueError
        from pydsl.Config import load
        self.grammarlist = []
        for x in grammarlist:
            if isinstance(x, str):
                self.grammarlist.append(load(x))
            else:
                self.grammarlist.append(x)
        from pydsl.Grammar.Definition import Grammar
        for x in self.grammarlist:
            if not isinstance(x, Grammar):
                raise TypeError("Expected GrammarDefinition, Got %s:%s" % (x.__class__.__name__,x))

    def __getitem__(self, index):
        """Retrieves token by index"""
        return self.grammarlist[index]

    @property
    def to_list(self):
        return self.grammarlist


class Encoding(Alphabet):
    """Defines an alphabet using an encoding string"""
    def __init__(self, encoding):
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


class ConceptAlphabet(Alphabet):
    """Stores a list of concepts"""
    def __init__(self, conceptlist):
        self.conceptlist = conceptlist

    def __getitem__(self, item):
        return self.conceptlist[item]

    @property
    def to_list(self):
        return self.conceptlist
