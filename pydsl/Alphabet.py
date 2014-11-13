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

import logging
LOG=logging.getLogger(__name__)

class Alphabet(set):
    """Uses a list of grammar definitions"""
    def __init__(self, grammarlist):
        set.__init__(self, grammarlist)
        self.original = grammarlist
        for x in self:
            from pydsl.Grammar.Definition import Grammar
            if not isinstance(x, Grammar):
                raise TypeError("Expected Grammar, Got %s:%s" % (x.__class__.__name__,x))

    def __str__(self):
        return str([str(x) for x in self])

    def __add__(self, other):
        return Alphabet(set.__add__(self, other))

    def __hash__(self):
        return hash(tuple(self.original))

    @property
    def minsize(self):
        return 1 #FIXME: In some cases could be 0

    @property
    def maxsize(self):
        return 1
