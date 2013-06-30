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


class GrammarDefinition(object):
    def __init__(self):
        pass

    def enum(self):
        """Generates every possible accepted string"""
        raise NotImplementedError

    @property
    def first(self):# -> set:
        """List of possible first elements"""
        return [x for x in self.alphabet().grammar_list]

    @property
    def minsize(self):# -> int:
        """Returns the minimum size in alphabet tokens"""
        return 0

    @property
    def maxsize(self):
        """Returns the max size in alphabet tokens"""
        return None

    def alphabet(self):
        """Returns the alphabet used by this grammar"""
        raise NotImplementedError

class PLYGrammar(GrammarDefinition):
    """PLY based grammar"""
    def __init__(self, module):
        GrammarDefinition.__init__(self)
        self.module = module

    @property
    def maxsize(self):
        raise NotImplementedError

    @property
    def minsize(self):
        raise NotImplementedError

class RegularExpressionDefinition(GrammarDefinition):
    def __init__(self, regexp, flags = 0):
        if not isinstance(regexp, str):
            raise TypeError
        GrammarDefinition.__init__(self)
        self.regexpstr = regexp
        self.flags = flags
        import re
        self.regexp = re.compile(regexp, flags)

    def __eq__(self, other):
        if not isinstance(other, RegularExpressionDefinition):
            return False
        return self.regexpstr == other.regexpstr and self.flags == other.flags
    @property
    def first(self):# -> set:
        i = 0
        while True:
            if self.regexpstr[i] == "^":
                i+=1
                continue
            if self.regexpstr[i] == "[":
                return [StringGrammarDefinition(x) for x in self.regexpstr[i+1:self.regexpstr.find("]")]]
            return [StringGrammarDefinition(self.regexpstr[i])]

    def __getattr__(self, attr):
        return getattr(self.regexp, attr)

    def alphabet(self):
        from pydsl.Alphabet.Definition import Encoding
        return Encoding("ascii")

class StringGrammarDefinition(GrammarDefinition):
    def __init__(self, string):
        GrammarDefinition.__init__(self)
        self.string = string

    def __hash__(self):
        return hash(self.string)

    def __eq__(self, other):
        try:
            return self.string == other.string
        except AttributeError:
            return False

    @property
    def first(self):
        return [StringGrammarDefinition(self.string[0])]

    def enum(self):
        yield self.string

    @property
    def maxsize(self):
        return len(self.string)

    @property
    def minsize(self):
        return len(self.string)

    def __str__(self):
        return str(self.string)

    def alphabet(self):
        return [StringGrammarDefinition(x) for x in self.string]

class JsonSchema(GrammarDefinition, dict):
    def __init__(self, *args, **kwargs):
        GrammarDefinition.__init__(self)
        dict.__init__(self, *args, **kwargs)

    def alphabet(self):
        from pydsl.Alphabet.Definition import Encoding
        return Encoding("ascii")

class MongoGrammar(GrammarDefinition, dict):
    def __init__(self, *args, **kwargs):
        GrammarDefinition.__init__(self)
        dict.__init__(self, *args, **kwargs)

    @property
    def first(self):
        return [StringGrammarDefinition("{")]

    def alphabet(self):
        from pydsl.Alphabet.Definition import Encoding
        return Encoding("ascii")

class PythonGrammar(GrammarDefinition, dict):
    def __init__(self, *args, **kwargs):
        GrammarDefinition.__init__(self)
        dict.__init__(self, *args, **kwargs)

    def alphabet(self):
        if "alphabet" in self:
            return self['alphabet']
        from pydsl.Alphabet.Definition import Encoding
        return Encoding("ascii")
