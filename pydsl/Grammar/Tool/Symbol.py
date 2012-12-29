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

import logging
from .Tool import GrammarTools
LOG = logging.getLogger("Grammar.Symbol")

class SymbolGrammarTools(GrammarTools):
    """Ask sentences to other grammars. Works with tokens"""
    def __init__(self, bnf, parser = "auto"):
        LOG.debug("SymbolGrammarTools.__init__: Begin")
        GrammarTools.__init__(self, bnf)
        parser = bnf.options.get("parser",parser)
        from pydsl.Memory.Loader import load_parser
        self.__parser = load_parser(bnf, parser)

    @property
    def productionset(self):
        """Returns parser productionset"""
        return self.__parser.productionset

    def groups(self):
        return [x.name for x in self.productionset.getSymbols()]

    def get_groups(self, word, propertyname):# -> list:
        """ Allow to ask for a grammar property of a valid sentence. Example: (English)ask for verb in a phrase: askProperty("verb","desk is clean") Maybe there is a method to pass it through __init__ (like _matchFun) """
        treelist = self.__parser.get_trees(word)
        for tree in treelist:
            if propertyname in tree:
                return tree.get_by_symbol(propertyname)
            return []

    def get_trees(self, word, showErrors = False): # -> list:
        """Returns a decomposition tree. askProperty and checkWord should rely on this
        parser returns DescentParserResult, but this function should return SymbolTokenTreeNode.
        It should work also for errors
        """
        return self.__parser.get_trees(word, showErrors)
    
    def genealogy(self, information, index): # -> list:
        """Given a word(token) index, will tell all parent symbols  until root node"""
        raise NotImplementedError

    def tokenize(self, information):
        #gets tree, then iterates through leaf nodes. 
        #TODO think about extra parameters for tree depth
        raise NotImplementedError
