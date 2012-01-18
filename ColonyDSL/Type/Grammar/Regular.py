#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of ColonyDSL.
#
#ColonyDSL is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#ColonyDSL is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with ColonyDSL.  If not, see <http://www.gnu.org/licenses/>.

"""Regular Expression Grammars"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@colonymbus.com"

#There are at least three ways to define a regular grammar. Regexp, FSM table, production rules. At this time, I'm going to combine several regexp rules, each one with a name.

import logging
from .Python import PythonGrammar
LOG = logging.getLogger("RegularGrammar")
CHARACTERS = {"a","b","c","d","e"}
ALLSYMBOLS = CHARACTERS.union({".",","})

#TODO: What if Terminal symbols in current grammar scope is a language-grammar-accepted word? We need to tell what terminal symbols mean

class RegularExpression:
    def __init__(self, regexpstring):
        self._regexpstring = regexpstring

class RegularExpressionGrammar(PythonGrammar, RegularExpression):
    def __init__(self, name, regexp, flags = ""):
        PythonGrammar.__init__(self, name, self._process_word)
        RegularExpression.__init__(self, regexp)
        import re
        self.__regexpstr = regexp
        myflags = 0
        if "i" in flags:
            myflags |= re.I
        self.__regexp = re.compile(regexp, myflags)

    def _process_word(self, word):
        """returns True if any match any regexp"""
        try:
            data = str(word)
        except UnicodeDecodeError:
            return False
        if data == "":
            return False
        if self.__regexp.match(data):
            return True
        return False

    def get_groups(self, word, groupname):
        """Match against specific rule"""
        data = str(word)
        if not data:
            return []
        groupdict = self.__regexp.match(data).groupdict()
        if not groupname in groupdict:
            return []
        return [(self.__regexp.match(data).start(groupname),self.__regexp.match(data).end(groupname))] #Returns a list

    def groups(self):
        return list(self.__regexp.groupindex.keys())

    def enumerate(self):
        """inspects regexp"""
        pass

    def iterate(self, information:str):
        """Uses python str iteration"""
        for x in information:
            yield x

    def alphabet(self):
        #FIXME:It is not working with groups
        index = 0
        result = set()
        while index < len(self.__regexpstr):
            if self.__regexpstr[index] == '\\':
                if self.__regexpstr[index+1] == '\\':
                    result.add('\\')
                elif self.__regexpstr[index+1] == 'w':
                    result = result.union(CHARACTERS)
                else:
                    result.add(self.__regexpstr[index+1])
                index += 2
                continue
            elif self.__regexpstr[index] == '.':
                result = result.union(ALLSYMBOLS)
            elif self.__regexpstr[index] == '*':  #TODO
                pass
            else:
                result.add(self.__regexpstr[index])
            index += 1
        return result

    @property
    def summary(self):
        return {"iclass":"RegularExpressionGrammar", "identifier":self.identifier, "groups":self.groups(), "regexp":self.__regexpstr}
