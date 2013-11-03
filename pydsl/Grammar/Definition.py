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
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"


class Grammar(object):

    def __init__(self):
        pass

    def enum(self):
        """Generates every possible accepted string"""
        raise NotImplementedError

    @property
    def first(self):# -> set:
        """Grammar definition with all possible first elements"""
        return self.alphabet()

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

class PLYGrammar(Grammar):
    """PLY based grammar"""
    def __init__(self, module):
        Grammar.__init__(self)
        self.module = module

    @property
    def maxsize(self):
        raise NotImplementedError

    @property
    def minsize(self):
        raise NotImplementedError

class RegularExpression(Grammar):
    def __init__(self, regexp, flags = 0):
        Grammar.__init__(self)
        import re
        retype = type(re.compile('hello, world'))
        if isinstance(regexp, retype):
            self.regexp = regexp
            self.regexpstr = regexp.pattern
            self.flags = regexp.flags
        elif isinstance(regexp, str):
            self.regexpstr = regexp
            self.flags = flags
            self.regexp = re.compile(regexp, flags)
        else:
            raise TypeError

    def __hash__(self):
        return hash(self.regexpstr)

    def __eq__(self, other):
        if not isinstance(other, RegularExpression):
            return False
        return self.regexpstr == other.regexpstr and self.flags == other.flags

    def __str__(self):
        return self.regexpstr

    @property
    def first(self):# -> set:
        i = 0
        while True:
            if self.regexpstr[i] == "^":
                i+=1
                continue
            if self.regexpstr[i] == "[":
                return [String(x) for x in self.regexpstr[i+1:self.regexpstr.find("]")]]
            return [String(self.regexpstr[i])]

    def __getattr__(self, attr):
        return getattr(self.regexp, attr)

    def alphabet(self):
        from pydsl.Alphabet import Encoding
        return Encoding("ascii")

class String(Grammar):
    def __init__(self, string):
        Grammar.__init__(self)
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
        return [String(self.string[0])]

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
        return [String(x) for x in self.string]

class JsonSchema(Grammar, dict):
    def __init__(self, *args, **kwargs):
        Grammar.__init__(self)
        dict.__init__(self, *args, **kwargs)

    def alphabet(self):
        from pydsl.Alphabet import Encoding
        return Encoding("ascii")

class MongoGrammar(Grammar, dict):
    def __init__(self, *args, **kwargs):
        Grammar.__init__(self)
        dict.__init__(self, *args, **kwargs)

    @property
    def first(self):
        return [String("{")]

    def alphabet(self):
        from pydsl.Alphabet import Encoding
        return Encoding("ascii")

class PythonGrammar(Grammar, dict):
    """
    A Python dictionary that defines a Grammar.
    it must define at least matchFun
    """
    def __init__(self, *args, **kwargs):
        """
        It receives a dictionary constructor which must define
        matchFun. Example: {'matchFun':<function x at 0x000000>}
        """
        Grammar.__init__(self)
        dict.__init__(self, *args, **kwargs)

    def __hash__(self):
        from pypository.utils import ImmutableDict #FIXME!
        return hash(ImmutableDict(self))        

    def alphabet(self):
        if "alphabet" in self:
            return self['alphabet']
        from pydsl.Alphabet import Encoding
        return Encoding("ascii")

def grammar_factory(input_definition):
    if isinstance(input_definition, str):
        return String(input_definition)
    import re
    retype = type(re.compile('hello, world'))
    if isinstance(input_definition, retype):
        return RegularExpression(retype)
    if isinstance(input_definition, collections.Iterable):
        if isinstance(input_definition[0], str):
            #Return a composition grammar ([a,b] -> "a|b")
            pass
        elif isinstance(input_definition[0], collections.Iterable):
            #
            pass
    raise ValueError("Unable to create a grammar for %s" % input_definition)
