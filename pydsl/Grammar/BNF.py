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

"""Production rules"""

from pydsl.Grammar.Symbol import Symbol, TerminalSymbol
from pydsl.Grammar.Definition import GrammarDefinition

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"


class Production:
    def __init__(self, leftside:list, rightside:list):
        #Left side must have at least one nonterminal symbol
        for element in rightside:
            if not isinstance(element, Symbol):
                raise TypeError
        self.leftside = leftside
        self.rightside = rightside

    def __str__(self):
        """Pretty print"""
        leftstr = ""
        rightstr = ""
        for symbol in self.leftside:
            leftstr += " " + symbol.name + " "
        for symbol in self.rightside:
            rightstr += " " + str(symbol) + " "
        return leftstr + " ::= " + rightstr

    def __eq__(self, other):
        try:
            if len(self.leftside) != len(other.leftside):
                return False
            if len(self.rightside) != len(other.rightside):
                return False
            for index in range(len(self.leftside)):
                if self.leftside[index] != other.leftside[index]:
                    return False
            for index in range(len(self.rightside)):
                if self.rightside[index] != other.rightside[index]:
                    return False
        except AttributeError:
            return False
        return True

    @property
    def name(self):
        if len(self.leftside) != 1:
            raise Exception
        return self.leftside[0].name


class BNFGrammar(GrammarDefinition): #Only stores a ruleset, and methods to ask properties or validity check 
    def __init__(self, initialsymbol, fulllist:list, options = {}):
        self._initialsymbol = initialsymbol
        for rule in fulllist:
            if fulllist.count(rule) >1:
                raise ValueError
        self.fulllist = fulllist
        self.options = options

    @property
    def productionlist(self):
        return [x for x in self.fulllist if isinstance(x, Production)]

    @property
    def terminalsymbollist(self):
        return [x for x in self.fulllist if isinstance(x,
            TerminalSymbol)]

    @property
    def left_recursive(self) -> bool:
        """Tests if exists left recursion"""
        #TODO
        raise NotImplementedError

    @property
    def right_recursive(self) -> bool:
        """Tests if exists right recursion"""
        #TODO
        raise NotImplementedError

    def __eq__(self, other):
        if not isinstance(other,BNFGrammar):
            return False
        if self._initialsymbol != other.initialsymbol:
            return False
        for index in range(len(self.productionlist)):
            if self.productionlist[index] != other.productionlist[index]:
                return False
        return True

    #def __getitem__(self, index):
    #    for rule in self.productionlist:
    #        if rule.name == index:
    #            return rule
    #    raise IndexError

    @property
    def initialsymbol(self):
        return self._initialsymbol

    @property
    def main_production(self):
        """Returns main rule"""
        for rule in self.productionlist:
            if rule.leftside[0] == self._initialsymbol:
                return rule
        raise IndexError

    def getProductionsBySide(self, symbollist:list, side = "left"):
        result = []
        for rule in self.productionlist: #FIXME Is iterating over production only
            part = None
            if side == "left":
                part = rule.leftside
            elif side == "right":
                part = rule.rightside
            else:
                raise KeyError
            valid = True
            if len(part) != len(symbollist):
                valid = False
            for ruleindex in range(len(part)):
                if part[ruleindex] != symbollist[ruleindex]:
                    valid = False
                    break
            if valid:
                result.append(rule)
        if not result:
            raise IndexError("Symbol: %s" % str([str(x) for x in symbollist]))

        return result

    def getProductionByBothSides(self, leftsymbollist:list, rightsymbollist:list):
        for rule in self.productionlist:
            valid = True
            if len(rule.leftside) != len(leftsymbollist):
                continue
            if len(rule.rightside) != len(rightsymbollist):
                continue
            for ruleindex in range(len(rule.leftside)):
                if leftsymbollist[ruleindex] != rule.leftside[ruleindex]:
                    valid = False
                    break
            if not valid:
                continue
            for ruleindex in range(len(rule.rightside)):
                if rightsymbollist[ruleindex] != rule.rightside[ruleindex]:
                    valid = False
                    break
            if not valid:
                continue
            if valid:
                return rule
        raise IndexError

    def getSymbols(self):
        """Returns every symbol"""
        symbollist = []
        for rule in self.productionlist:
            for symbol in rule.leftside + rule.rightside:
                if symbol not in symbollist:
                    symbollist.append(symbol)
        symbollist += self.terminalsymbollist
        return symbollist

    def getProductions(self):
        return self.productionlist

    def getTerminalSymbols(self):
        """Returns a list with every terminal symbol """
        return self.terminalsymbollist

    def getProductionIndex(self, rule):
        return self.productionlist.index(rule)

    def __str__(self):
        return str(list(map(str,self.productionlist)))

def create_non_terminal_production(productionset:list, terminalsymbol):
    """Creates a new nonterminalrule for terminalsymbol
    A -> B,nt 
    is changed to: 
    A -> B,C  
    C -> nt
    """
    #walks through all rules looking for our terminalsymbol in rightside
    from .Symbol import NonTerminalSymbol
    productionstochange = []
    for index, production in enumerate(productionset[:]): #copy
        if terminalsymbol in production.rightside:
            for symbol in production.rightside:
                if isinstance(symbol, NonTerminalSymbol):
                    productionstochange.append(production)
                    del productionset[index]
                    break
    #Inserts new rule
    newsymbol = NonTerminalSymbol(str(terminalsymbol))
    newproduction = Production(newsymbol, terminalsymbol)
    productionset.append(newproduction)
    #modifies required rules to link with new production
    for production in productionstochange:
        newproduction = Production(production.leftside[:], production.rightside[:])
        for index, element in enumerate(production.rightside):
            if element == terminalsymbol:
                del newproduction.rightside[index]
                newproduction.rightside.insert(index, newsymbol)
        productionset.append(newproduction)
    return productionset

def reduce_non_terminal_production(productionset:list, uselesssymbol):
    """search for production that only have nonterminalsymbol at right, subst nonterminal from rules at right and  remove the rule that have it at left"""
    production = productionset.getProductionsBySide(uselesssymbol, "right")
    productionset.remove(production)
    validterminalsymbol = production.leftside[0] #usefulterminalymbol
    productionlist = productionset.getProductionsBySide(uselesssymbol)
    saverule = False

    if len(productionlist) > 1:
        saverule = True
        #several rules with uselesssymbol at left

    for production in productionset:    
        if uselessnonterminal in production.rightside:
            #adds those who have nonterminal at right 
            newproduction = production.copy()
            index = newproduction.index(uselessnonterminal)
            del newproduction[index]
            newproduction.insert(index, validterminalsymbol)
            if not saverule:#Si no habia otra produccion
                productionset.remove(production)


def split_production(productionset:list, production):
    from .Symbol import NonTerminalSymbol
    if len(production.rightside) < 2:
        return productionset
    index = 0
    productionset.remove(production)
    newrightside = []
    while index < len(production) - 2:
        firsttwo = production.rightside[index:index+2]
        newsymbol = NonTerminalSymbol(production.leftside[0].name + "E")
        newrightside.append(newsymbol)
        newproduction = Production(newsymbol, firsttwo)
        productionset.append(newproduction)
        index += 2
    newrightside += production.rightside[index:]
    newproduction = Production(production.leftside, newrightside)
    productionset.append(newproduction)
    return productionset


def chomsky_normal_form(productionset:BNFGrammar) -> BNFGrammar:
    """TODO Check is Epsilon free"""
    ntermslist = []
    from .Symbol import NonTerminalSymbol
    #STEP 1: A -> B,c 
    #Terminal and nonterminal at right side 
    for production in productionset:
        termlist = 0
        ntermlist = 0
        for element in production.rightside:
            if isinstance(element, TerminalSymbol):
                termlist.append(element)
            elif isinstance(element, NonTerminalSymbol):
                ntermlist.append(element)
        if termlist and ntermlist:
            ntermslist += termlist
    for terminal in ntermlist:
        productionset = create_non_terminal_production(productionset, terminal)
    #STEP 2: useless nonterminal
    uselessnonterms = []
    for production in productionset:
        if len(production.rightside) == 1 and isinstance(production.rightside[0], NonTerminalSymbol):
            uselessnonterms.append(production.rightside[0])
    for nonterm in uselessnonterms:
        productionset = reduce_non_terminal_production(productionset, nonterm)

    #STEP 3:rightside is too long 
    longproductions = []
    for production in productionset:
        if len(production.rightside) > 2:
            longproductions.append(production)
    for production in longproductions:
        productionset = split_production(productionset, nonterm)

    return productionset
