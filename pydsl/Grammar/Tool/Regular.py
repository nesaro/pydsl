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

"""Regular Expression Grammars"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"

#There are at least three ways to define a regular grammar. Regexp, FSM table, production rules. At this time, I'm going to combine several regexp rules, each one with a name.

import logging
from .Tool import GrammarTools
import re
LOG = logging.getLogger(__name__)
CHARACTERS = {"a","b","c","d","e"}
ALLSYMBOLS = CHARACTERS.union({".",","})

#TODO: What if Terminal symbols in current grammar scope is a language-grammar-accepted word? We need to tell what terminal symbols mean

def regexp_alphabet_helper(string, endchar = None) -> set:
    index = 0
    result = set()
    while index < len(string):
        if string[index] == '\\':
            if string[index+1] == '\\':
                result.add('\\')
            elif string[index+1] == 'w':
                result = result.union(CHARACTERS)
            else:
                result.add(string[index+1])
            index += 2
            continue
        elif string[index] == endchar:
            return result, index
        elif string[index] == '.':
            result = result.union(ALLSYMBOLS)
        elif string[index] == '*':  
            pass
        elif string[index] == '?':  
            pass
        elif string[index] == '<':
            newresult, newindex = regexp_alphabet_helper(string[index+1:], ">")
            index += newindex + 1
        elif string[index] == '(':
            if string[index+1:index+3] == "?P":
                index += 2
            newresult, newindex =regexp_alphabet_helper(string[index+1:], ")")
            result = result.union(newresult)
            index += newindex + 1
        else:
            result.add(string[index])
        index += 1
    return result, index

class RegularExpressionGrammarTools(GrammarTools):
    def __init__(self, regexp, flags = ""):
        GrammarTools.__init__(self)
        if isinstance(regexp, str):
            from pydsl.Grammar.Definition import RegularExpressionDefinition
            regexp = RegularExpressionDefinition(regexp)
        self.__gd = regexp

    def check(self, word):
        from ..Checker import RegularExpressionChecker
        checker = RegularExpressionChecker(self.__gd)
        return checker.check(word)

    def get_groups(self, word, groupname):
        """Match against specific rule"""
        data = str(word)
        if not data:
            return []
        groupdict = self.__gd.match(data).groupdict()
        if not groupname in groupdict:
            return []
        return [(self.__gd.match(data).start(groupname),self.__gd.match(data).end(groupname))] #Returns a list

    def groups(self):
        return list(self.__gd.groupindex.keys())

    def tokenize(self, information:str):
        """Uses python str iteration"""
        for x in information:
            yield x

    def alphabet(self):
        #FIXME:It is not working with groups
        return regexp_alphabet_helper(self.__gd.regexpstr)[0]

    @property
    def summary(self):
        return {"iclass":"RegularExpressionGrammar", "groups":self.groups(), "regexp":self.__gd}
