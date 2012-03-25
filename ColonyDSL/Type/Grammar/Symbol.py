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

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

import logging
from .Grammar import Grammar
LOG = logging.getLogger("Grammar.Symbol")

class SymbolGrammar(Grammar):
    """Ask sentences to other grammars. Works with tokens"""
    def __init__(self, identifier, productionset, parser = "auto"):
        LOG.debug("SymbolGrammar.__init__: Begin")
        Grammar.__init__(self)
        if parser == "descent":
            from .Parser.RecursiveDescent import RecursiveDescentParser
            self.__parser = RecursiveDescentParser(productionset)
        elif parser == "weighted":
            self.__parser = WeightedParser(productionset)
            raise Exception
        elif parser == "auto" or parser == "default":
            #TODO Guess best parser
            from .Parser.Weighted import WeightedParser
            self.__parser = RecursiveDescentParser(productionset)
        else:
            LOG.error("Wrong parser name: " + parser)
            raise Exception

    @property
    def productionset(self):
        """Returns parser productionset"""
        return self.__parser.productionset

    def groups(self):
        return [x.name for x in self.productionset.getSymbols()]

    def get_groups(self, word, propertyname:str) -> list:
        """ Allow to ask for a grammar property of a valid sentence. Example: (English)ask for verb in a phrase: askProperty("verb","desk is clean") Maybe there is a method to pass it through __init__ (like _matchFun) """
        treelist = self.__parser.get_trees(word)
        for tree in treelist:
            from ColonyDSL.Type.Grammar.Tree import parser_to_post_tree
            posttree = parser_to_post_tree(tree)
            if propertyname in posttree:
                return posttree[propertyname] 
            else:
                return []

    def get_trees(self, word, showErrors = False) -> list:
        """Returns a decomposition tree. askProperty and checkWord should rely on this
        parser returns DescentParserResult, but this function should return SymbolTokenTreeNode.
        It should work also for errors
        """
        return self.__parser.get_trees(word, showErrors)
    
    def alphabet(self):
        #TODO
        return set()
    
    @property
    def summary(self):
        return {"iclass":"SymbolGrammar", "identifier":self.identifier, "groups":tuple(self.groups())}

    def check(self, word):
        from .Result import DiscreteGrammarResult
        try:
            return DiscreteGrammarResult(self.__parser.check(word))
        except IndexError:
            LOG.exception("EXCEPTION IndexError")
            return DiscreteGrammarResult(False) #TODO: grammar definition will tell what to do when is ambiguous
        return DiscreteGrammarResult(False)


    def genealogy(self, information, index) -> list:
        """Given a word(token) index, will tell all parent symbols  until root node"""
        raise NotImplementedError

    def iterate(self, information):
        #gets tree, then iterates through leaf nodes. 
        #TODO think about extra parameters for tree depth
        raise NotImplementedError
