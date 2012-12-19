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



"""Syntax Directed Transformers"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)

class SyntaxDirectedTransformer:
    def __init__(self, inputgrammar, outputgrammar, blockdic):
        self.blockdic = blockdic
        if isinstance(inputgrammar, str):
            from pydsl.Memory.Loader import load
            inputgrammar = load(inputgrammar)
        from pydsl.Grammar.Parser.RecursiveDescent import RecursiveDescentParser
        self.parser = RecursiveDescentParser(inputgrammar)
        self.blockdic = blockdic

    def __parseSymbolTokenTree(self, stt):
        """Returns a tokenlist"""
        #productionruleset = list(self.inputchanneldic.values())[0].productionset
        from pydsl.Grammar.Symbol import TerminalSymbol
        if isinstance(stt.production, TerminalSymbol):
            return stt.content
        childlist = []
        for child in stt.childlist:
            childlist.append(self.__parseSymbolTokenTree(child))
        if not str(stt.production) in self.blockdic and len(childlist) == 1:
            return childlist[0]
        return self.blockdic[str(stt.production)](childlist)

    def __call__(self, word):
        stt = self.parser.get_trees(word)[0]
        return self.__parseSymbolTokenTree(stt)

    @property
    def summary(self):
        return {"iclass":"SyntaxDirectedTransformer", "identifier":self.identifier, "input":self.inputgrammar, "output":self.outputgrammar }
