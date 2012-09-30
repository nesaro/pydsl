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

"""Python Function Grammar"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

from .Tool import GrammarTools
import logging
LOG = logging.getLogger(__name__)

class PythonGrammarTools(GrammarTools):
    def __init__(self, dictionary):
        GrammarTools.__init__(self)
        self.dictionary = dictionary
        self._matchFun = None
        self._askprop = dictionary.get('propFun')
        self._enumFun = dictionary.get('enumFun')
        self._alphabetFun = dictionary.get('alphabetFun')

    def check(self, word):
        if not self._matchFun:
            from pydsl.Memory.Loader import load_checker
            self._matchFun = load_checker(self.dictionary)
        return self._matchFun.check(word)

    def get_groups(self, word, propertyname):
        if self._askprop != None:
            return [self._askprop(word, propertyname)]
        return []

    def enum(self):
        if self._enumFun != None:
            return set(self._enumFun())
        return set()

    def tokenize(self, data):
        if self._iterFun != None:
            for x in self._iterFun(data):
                yield x

    @property
    def alphabet(self) -> set:
        if self._alphabetFun != None:
            return set(self._alphabetFun())
        return set()

    @property
    def summary(self):
        return {"iclass":"PythonGrammar", "ancestors":self.ancestors() }

