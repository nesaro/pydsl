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
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"


class GrammarDefinition(object):
    def __init__(self):
        pass

    def enum(self):
        raise NotImplementedError

    @property
    def first(self):# -> set:
        raise NotImplementedError

    @property
    def minsize(self):# -> int:
        return 0

    @property
    def maxsize(self):
        return None

    def alphabet(self):
        """Returns the alphabet required by this grammar"""
        raise NotImplementedError

class PLYGrammar(GrammarDefinition):
    """PLY based grammar"""
    def __init__(self, module):
        GrammarDefinition.__init__(self)
        self.module = module

    @property
    def maxsize(self):
        pass

    @property
    def minsize(self):
        pass

class RegularExpressionDefinition(GrammarDefinition):
    def __init__(self, regexp, flags = 0):
        if not isinstance(regexp, str):
            raise TypeError
        GrammarDefinition.__init__(self)
        self.regexpstr = regexp
        self.flags = flags
        import re
        self.regexp = re.compile(regexp, flags)

    @property
    def first(self):# -> set:
        i = 0
        while True:
            if self.regexpstr[i] == "^":
                i+=1
                continue
            if self.regexpstr[i] == "[":
                return [x for x in self.regexpstr[i+1:self.regexpstr.find("]")]]
            return self.regexpstr[i] 

    def __getattr__(self, attr):
        return getattr(self.regexp, attr)

class JsonSchema(GrammarDefinition, dict):
    pass

class MongoGrammar(GrammarDefinition, dict):
    @property
    def first(self):
        return "{"
