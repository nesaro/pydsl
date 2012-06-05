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

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

from .Tool import GrammarTools
from pydsl.Abstract import Indexable
import logging
LOG = logging.getLogger(__name__)

class PythonGrammarTools(GrammarTools, Indexable):
    def __init__(self, matchFun, propFun = None, enumFun = None, alphabetFun = None):
        GrammarTools.__init__(self)
        self._matchFun = matchFun
        self._askprop = propFun
        self._enumFun = enumFun
        self._alphabetFun = alphabetFun

    def check(self, word):
        if not self._matchFun:
            return False #Match function isn't defined
        try:
            return self._matchFun(word)
        except UnicodeDecodeError:
            return False

    def get_groups(self, word, propertyname):
        if self._askprop != None:
            return [self._askprop(word, propertyname)]
        return []

    def enumerate(self):
        if self._enumFun != None:
            return set(self._enumFun())
        return set()

    def iterate(self, data):
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

class HostPythonGrammarTools(PythonGrammarTools):
    def __init__(self, matchFun, auxdic, propFun = None):
        PythonGrammarTools.__init__(self, matchFun, propFun)
        self.auxgrammar = {}
        from pydsl.Memory.Storage.Loader import load_grammar
        for key, value in auxdic.items():
            self.auxgrammar[key] = load_grammar(value)

    def check(self, word):
        if not self._matchFun:
            return False #Match function isn't defined
        try:
            return self._matchFun(word, self.auxgrammar)
        except UnicodeDecodeError:
            LOG.exception("Unicode Error while calling matchfun")
            return False
        

