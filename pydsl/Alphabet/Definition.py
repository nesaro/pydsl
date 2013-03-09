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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"


class AlphabetDefinition(object):
    """Defines an alphabet"""
    @property
    def grammar_list(self):
        """Returns a list of allowed grammars"""
        raise NotImplementedError

    def __contains__(self, token):
        """Returns true if the alphabet contains the token"""
        raise NotImplementedError

class AlphabetListDefinition(AlphabetDefinition):
    """Uses a list of grammardefinitions"""
    def __init__(self, grammarlist):
        if not grammarlist:
            raise ValueError
        self.grammarlist = grammarlist

    def __getitem__(self, index):
        """Retrieves token by index"""
        return self.grammarlist[index]

    @property
    def grammar_list(self):
        return self.grammarlist


class AlphabetDictDefinition(AlphabetDefinition):
    """Uses a dict of grammardefinitions"""
    def __init__(self, grammarlist):
        if not grammarlist:
            raise ValueError
        from pydsl.Memory.Loader import load
        self.grammardict = {}
        for x in grammarlist:
            self.grammardict[x] = load(grammarlist[x])

    def __getitem__(self, item):
        """Retrieves token by name"""
        from pydsl.Grammar.Definition import StringGrammarDefinition
        return StringGrammarDefinition(self.grammardict[item])

    @property
    def grammar_list(self):
        return list(self.grammardict.keys())

class Encoding(AlphabetDefinition):
    """Defines an alphabet using an encoding string"""
    def __init__(self, encoding):
        self.encoding = encoding

    def __getitem__(self, item):
        from pydsl.Checker import EncodingChecker
        if EncodingChecker(self).check(item):
            from pydsl.Grammar.Definition import StringGrammarDefinition
            return StringGrammarDefinition(item)
        raise KeyError
