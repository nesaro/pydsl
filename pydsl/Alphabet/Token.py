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

from pydsl.Grammar.Definition import StringGrammarDefinition

class Token(object):
    """ Stores a token and its associated, grammardefinition """
    def __init__(self, string, gd=None):
        if gd is None:
            self.gd = StringGrammarDefinition(string)
        else:
            self.gd = gd
        self.string = string

    def __str__(self):
        return self.string

    def __eq__(self, other):
        try:
            return self.gd == other.gd and self.string == other.string
        except AttributeError:
            return False

class TokenList(list):
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        for x in self:
            if not isinstance(x, Token):
                raise TypeError(x)
    def __bool__(self):
        return len(self) > 1

    def __str__(self):
        return "".join([str(x) for x in self]) #TODO delete the EOF element

