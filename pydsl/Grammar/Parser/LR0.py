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

"""LR0 unfinished implementation"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pydsl.Grammar.Parser.Parser import BottomUpParser
from pydsl.Grammar.Symbol import NonTerminalSymbol, TerminalSymbol, EndSymbol, Symbol
from pydsl.Grammar.BNF import NonTerminalProduction

def __check_action(action):
    """Valid actions string"""
    return action in ["Accept", "Shift", "Reduce", "Fail"]

def __build_item_closure(itemset, productionruleset):
    """Build input itemset closure """
    #For every item inside current itemset, if we have the following rule:
    #  xxx <cursor><nonterminalSymbol> xxx  append every rule from self._productionruleset that begins with that NonTerminalSymbol
    LOG.debug("__build_item_closure: Begin")
    if not isinstance(itemset, LR0ItemSet):
        raise TypeError
    import copy
    resultset = copy.copy(itemset)
    changed = True
    while changed:
        changed = False
        for currentitem in resultset.itemlist:
            nextsymbol = currentitem.next_symbol()
            if nextsymbol is None:
                break
            for rule in productionruleset.productionrulelist:
                if rule.leftside[0] == nextsymbol:
                    newitem = LR0Item(rule, 0)
                    if newitem not in resultset.itemlist:
                        resultset.append_item(newitem)
                        changed = True
                if rule.rightside[0] == nextsymbol:
                    newitem = LR0Item(rule, 0)
                    if newitem not in resultset.itemlist:
                        resultset.append_item(newitem)
                        changed = True
    return resultset

def item_set_goto(itemset, inputsymbol, productionruleset):
    """returns an itemset
    locate inside itemset every element with inputsymbol following cursor
    for every located item, append its itemclosure"""
    resultset = LR0ItemSet()
    for item in itemset.itemlist:
        if item.next_symbol() == inputsymbol:
            newitem = LR0Item(item.rule, item.position + 1)
            resultset.append_item(newitem)
    return __build_item_closure(resultset, productionruleset)

def build_states_sets(productionruleset):
    """Build states sets"""
    LOG.debug("buildStatesSets: Begin")
    result = []
    symbollist = productionruleset.getSymbols()
    #mainproductionrule = productionruleset.getMainRule()
    mainproductionrule = NonTerminalProduction("Extended initial", [NonTerminalSymbol("EI")] , [productionruleset.getInitialSymbol()])
    mainproductionruleitem = LR0Item(mainproductionrule, 0)
    mainproductionruleitemset = LR0ItemSet()
    mainproductionruleitemset.append_item(mainproductionruleitem)
    index0 = __build_item_closure(mainproductionruleitemset, productionruleset)
    LOG.debug("buildStatesSets: mainsymbol closure: " + str(index0))
    result.append(index0)
    changed = True
    #returns a set of itemsets
    while changed:
        changed = False
        for itemset in result:
            for symbol in symbollist:
                if symbol in itemset:
                    break
                newitemset = item_set_goto(itemset, symbol, productionruleset)
                found = False
                for curreintitemset in result:
                    if curreintitemset == newitemset:
                        found = True
                        changed = True
                        itemset.append_transition(symbol, curreintitemset)
                        break
                if not found and (newitemset not in result):
                    changed = True
                    result.append(newitemset)
                    itemset.append_transition(symbol, newitemset)
    return result

def __slr_build_parser_table(productionruleset):
    """SLR method to build parser table"""
    LOG.debug("__slr_build_parser_table: Begin")
    result = ParserTable()
    #when buildStatesSets finishes its job
    statesset = build_states_sets(productionruleset)
    for itemindex in range(len(statesset)):
        itemset = statesset[itemindex]
        LOG.debug("__slr_build_parser_table: Evaluating itemset:" + str(itemset))
        for symbol in productionruleset.getTerminalSymbols() + [EndSymbol]:
            numberoptions = 0
            for lritem in itemset.itemlist:
                #if cursor is before a terminal, and there is a transition to another itemset with the following terminal, append shift rule
                if isinstance(symbol, TerminalSymbol) and lritem.next_symbol() == symbol and symbol in itemset:
                    destinationstate = statesset.index(itemset.get_transition(symbol))
                    result.append_rule(itemindex, symbol, "Shift", destinationstate)
                    numberoptions += 1
                #if cursor is at the end of the rule, then append reduce rule and go transition
                if lritem.previous_symbol() == symbol and lritem.is_last_position() and symbol != productionruleset.getInitialSymbol():
                    result.append_reduction(itemindex, symbol, itemindex, lritem)
                    numberoptions += 1
                #if cursor is at the end of main rule, and current symbol is end, then append accept rule
                if isinstance(symbol, EndSymbol) and lritem.is_last_position() and symbol == productionruleset.getInitialSymbol():
                    result.append_rule(itemindex, symbol, "Accept", itemindex)
                    numberoptions += 1
            if numberoptions == 0:
                LOG.debug("No rule found to generate a new parsertable entry ")
                LOG.debug("symbol: " + str(symbol))
                LOG.debug("itemset: " + str(itemset))
            if numberoptions > 1:
                from pydsl.Exceptions import LRConflictException
                raise LRConflictException
    return result
    
class ParserTable(object):
    """ Stores a state/symbol/action/new state relation """
    def __init__(self):
        self.__internalstate = None
        self.set_initial_state()
        #Default for every state: Fail state
        self.__table = {}

    def __str__(self):
        return "<ParserTable - State:" + str(self.__internalstate) + " Table: " + str(self.__table) + ">"

    def append_rule(self, state, symbol, action, destinationstate):
        """Appends a new rule"""
        if not __check_action(action) or action == "Reduce":
            raise TypeError
        if not state in self.__table:
            self.__table[state] = {}
        self.__table[state][symbol.name] = {"action":action, "dest":destinationstate}

    def append_reduction(self, state, symbol, destinationstate, rule):
        """Appends a reduce action. It also stores which ProductionRule must follow on reduction"""
        if not state in self.__table:
            self.__table[state] = {}
        self.__table[state][symbol.name] = {"action":"Reduce", "dest":destinationstate, "rule":rule}

    def current_state(self):
        """returns current state"""
        return self.__internalstate

    def insert_symbol(self, symbol):
        """change internal state, return action"""
        if not isinstance(symbol, Symbol):
            LOG.error("Bad arg for insert_symbol function")
            raise TypeError
        if self.__internalstate not in self.__table:
            raise IndexError
        if symbol not in self.__table[self.__internalstate]:
            self.set_initial_state()
            return {"action":"Fail"}
        result = self.__table[self.__internalstate, symbol]
        newstate = result["dest"]
        self.__internalstate = newstate
        return result
        
    def set_initial_state(self):
        """sets initial state to 0"""
        self.__internalstate = 0


class LR0Item(object):
    """LR0 table item"""
    def __init__(self, rule, cursorposition):
        if not isinstance(rule, NonTerminalProduction):
            raise TypeError
        self.rule = rule
        self.position = cursorposition
        #TODO: Verificar que la posicion es menor o igual que la longitud de la parte derecha de la regla

    def __str__(self):
        return "<LR0Item - Rule: " + str(self.rule) + " Position: " + str(self.position) + ">"

    def __eq__(self, other):
        if not isinstance(other, LR0Item):
            raise TypeError
        if self.position != other.position:
            return False
        if self.rule != other.rule:
            return False
        return True

    def previous_symbol(self):
        """returns cursor's previous symbol"""
        if self.position == 0:
            return None
        return self.rule.rightside[self.position-1]

    def next_symbol(self):
        """returns the symbol located after cursor"""
        try:
            return self.rule.rightside[self.position]
        except IndexError:
            return None

    def is_last_position(self):
        """Returns true if cursor if after last element"""
        return self.position > len(self.rule.rightside)

class LR0ItemSet(object):
    """Stores LR0Items, and a dic with symbols and destination states"""
    def __init__(self):
        self.itemlist = []
        self.__transitiondic = {}

    def __str__(self):
        result = "<LR0ItemSet: \n"
        for item in self.itemlist:
            result += str(item) + ","
        result += "transitions:" + str(self.__transitiondic)
        result += ">"
        return result

    def __eq__(self, anotherset):
        """Tests on itemlist equality"""
        if not isinstance(anotherset, LR0ItemSet):
            raise TypeError
        if len(self.itemlist) != len(anotherset.itemlist):
            return False
        for element in self.itemlist:
            if element not in anotherset.itemlist:
                return False
        return True

    def append_item(self, item):
        """Apend new item to set"""
        if not isinstance(item, LR0Item):
            raise TypeError
        self.itemlist.append(item)

    def append_transition(self, symbol, targetset):
        """Appends a transition"""
        if symbol.name in self.__transitiondic:
            return
        self.__transitiondic[symbol.name] = targetset

    def __contains__(self, symbol):
        return symbol.name in self.__transitiondic

    def get_transition(self, symbol):
        """gets a transition"""
        return self.__transitiondic[symbol.name]

class LR0Parser(BottomUpParser):
    """LR0 bottomup parser. Not finished"""
    def __init__(self, productionruleset):
        #TODO: Build extended productionruleset before calling parent constructor
        BottomUpParser.__init__(self, productionruleset)
        self.__stack = [] 
        #Add main item to itemsclosure with cursor at 0 position
        self.__parsertable = __slr_build_parser_table(productionruleset)
        #build GoTo and Action Table from ProductionRuleSet

    def check_word(self, tokenlist):
        """see parent docstring"""
        LOG.debug("check_word: Begin")
        self.__parsertable.set_initial_state()
        #empty stack

        #convert tokens to terminalsymbols
        #iterate over symbollist
        LOG.debug("check_word: checking list: " + str(tokenlist))
        for token in tokenlist:
            newdic = self.__parsertable.insert_symbol(token)
            currentstate = self.__parsertable.current_state()
            action = newdic["action"]
            if action == "Reduce":
                reductionrule = newdic["rule"]
                #TODO extract len(right side) of the rule and insert left side
                for unused in range(len(reductionrule.rightside)):
                    self.__stack.pop()
                self.__stack.append((currentstate, reductionrule.leftside))
            if action == "Shift":
                self.__stack.append((currentstate, token))
            if action == "Fail":
                return False
            if action == "Accept":
                return True
        return False


    def get_symbol_token_map(self, tokenlist):
        """ returns a SymbolTokenMap with best guesses """
        #Symbol to token map can be retrieved from parsertable. It must store left side of rule on reduction 
        #TODO : think about this
        pass

