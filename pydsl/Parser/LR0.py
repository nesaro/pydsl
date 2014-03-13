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

"""SLR0 implementation"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pydsl.Parser.Parser import BottomUpParser
from pydsl.Grammar.Symbol import NonTerminalSymbol, TerminalSymbol, EndSymbol, Symbol
from pydsl.Grammar.BNF import Production

Extended_S = NonTerminalSymbol("EI")

def _build_item_closure(itemset, productionset):
    """Build input itemset closure """
    #For every item inside current itemset, if we have the following rule:
    #  xxx <cursor><nonterminalSymbol> xxx  append every rule from self._productionruleset that begins with that NonTerminalSymbol
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
            for rule in productionset.productions:
                newitem = LR0Item(rule)
                if rule.leftside[0] == nextsymbol and newitem not in resultset.itemlist:
                    resultset.append_item(newitem)
                    changed = True
    return resultset

def item_set_goto(itemset, inputsymbol, productionset):
    """returns an itemset
    locate inside itemset every element with inputsymbol following cursor
    for every located item, append its itemclosure"""
    resultset = LR0ItemSet()
    for item in itemset.itemlist:
        if item.next_symbol() == inputsymbol:
            newitem = LR0Item(item.rule, item.position + 1)
            resultset.append_item(newitem)
    return _build_item_closure(resultset, productionset)

def build_states_sets(productionset):
    symbollist = productionset.getSymbols() + [EndSymbol()]
    mainproductionrule =  Production([Extended_S] , [productionset.initialsymbol, EndSymbol()])
    mainproductionruleitem = LR0Item(mainproductionrule)
    mainproductionruleitemset = LR0ItemSet()
    mainproductionruleitemset.append_item(mainproductionruleitem)
    index0 = _build_item_closure(mainproductionruleitemset, productionset)
    LOG.debug("buildStatesSets: mainsymbol closure: " + str(index0))
    result = [index0]
    changed = True
    #returns a set of itemsets
    while changed:
        changed = False
        for itemset in result[:]:
            for symbol in symbollist:
                if itemset.has_transition(symbol): #FIXME a symbol in a LR0item list?
                    continue
                newitemset = item_set_goto(itemset, symbol, productionset)
                if newitemset in result and itemset.has_transition(symbol) and itemset.get_transition(symbol) != newitemset:
                    changed = True
                    itemset.append_transition(symbol, newitemset)
                elif newitemset in result and not itemset.has_transition(symbol):
                    changed = True
                    itemset.append_transition(symbol, newitemset)
                elif newitemset and newitemset not in result: #avoid adding a duplicated entry
                    changed = True
                    result.append(newitemset)
                    itemset.append_transition(symbol, newitemset)
    return result

def _slr_build_parser_table(productionset):
    """SLR method to build parser table"""
    result = ParserTable()
    statesset = build_states_sets(productionset)
    for itemindex, itemset in enumerate(statesset):
        LOG.debug("_slr_build_parser_table: Evaluating itemset:" + str(itemset))
        for symbol in productionset.getSymbols() + [EndSymbol()]:
            numberoptions = 0
            for lritem in itemset.itemlist:
                #if cursor is before a terminal, and there is a transition to another itemset with the following terminal, append shift rule
                if isinstance(symbol, TerminalSymbol) and lritem.next_symbol() == symbol and itemset.has_transition(symbol):
                    destinationstate = statesset.index(itemset.get_transition(symbol))
                    result.append(itemindex, symbol, "Shift", destinationstate)
                    numberoptions += 1
                if isinstance(symbol, NonTerminalSymbol) and lritem.next_symbol() == symbol and itemset.has_transition(symbol):
                    destinationstate = statesset.index(itemset.get_transition(symbol))
                    result.append_goto(itemindex, symbol, destinationstate)
                #if cursor is at the end of the rule, then append reduce rule and go transition
                if lritem.previous_symbol() == symbol and lritem.is_last_position() and symbol != Extended_S:
                    for x in productionset.next_lookup(symbol):
                        from pydsl.Grammar.Definition import String
                        if isinstance(x, list):
                            result.append(itemindex, TerminalSymbol(String(x[0])), "Reduce", None, lritem.rule)
                        else:
                            result.append(itemindex, TerminalSymbol(String(x)), "Reduce", None, lritem.rule)
                    numberoptions += 1
                #if cursor is at the end of main rule, and current symbol is end, then append accept rule
                if isinstance(symbol, EndSymbol) and lritem.previous_symbol() == productionset.initialsymbol and lritem.next_symbol() == EndSymbol():
                    result.append(itemindex, symbol, "Accept", None)
                    numberoptions += 1
            if not numberoptions:
                LOG.info("No rule found to generate a new parsertable entry ")
                LOG.debug("symbol: " + str(symbol))
                LOG.debug("itemset: " + str(itemset))
            elif numberoptions > 1: #FIXME can it count duplicated entries?
                raise Exception("LR Conflict %s" % symbol)
    return result
    
class ParserTable(dict):
    """ Stores a state/symbol/action/new state relation """
    #Default for every state: Fail state #FIXME use default_dict

    def append(self, state, symbol, action, destinationstate, production = None):
        """Appends a new rule"""
        if action not in (None, "Accept", "Shift", "Reduce"):
            raise TypeError
        if not state in self:
            self[state] = {}
        rule = {"action":action, "dest":destinationstate}
        if action == "Reduce":
            if rule is None:
                raise TypeError("Expected production parameter")
            rule["rule"] = production
        if isinstance(symbol, list) and len(symbol) == 1:
            symbol = symbol[0]
        if not isinstance(symbol, Symbol):
            raise TypeError("Expected symbol, got %s" % symbol)
        self[state][symbol] = rule

    def append_goto(self, state, symbol, destinationstate):
        if not state in self:
            self[state] = {}
        if symbol in self[state] and self[state][symbol] != destinationstate:
            raise Exception
        self[state][symbol] = destinationstate

    def goto(self, state, symbol):
        return self[state][symbol]

    def insert(self, state, token):
        """change internal state, return action"""
        for symbol in self[state]:
            from pydsl.Check import check
            if symbol == EndSymbol() or isinstance(symbol, TerminalSymbol) and check(symbol.gd,token):
                break
        else:
            if token != EndSymbol():
                return {"action":"Fail"}
            else:
                symbol = EndSymbol()
        try:
            return self[state][symbol]
        except KeyError:
            return {"action":"Fail"}



class LR0Item(object):
    """LR0 table item"""
    def __init__(self, rule, position = 0):
        if not isinstance(rule, Production):
            raise TypeError
        if position > len(rule.rightside):
            raise ValueError("Position is outside the rule")
        self.rule = rule
        self.position = position

    def __str__(self):
        rscopy = [str(x) for x in self.rule.rightside]
        rscopy.insert(self.position, ".")
        return str([str(x) for x in self.rule.leftside]) + ": " + str(rscopy) 

    def __eq__(self, other):
        if not isinstance(other, LR0Item):
            return False
        return self.position == other.position and self.rule == other.rule

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
        return self.position >= len(self.rule.rightside)

class LR0ItemSet(object):
    """Stores LR0Items, and a dic with symbols and destination states"""
    def __init__(self):
        self.itemlist = []
        self.transitions = {}

    def __str__(self):
        result = "<LR0ItemSet: \n"
        for item in self.itemlist:
            result += str(item) + ","
        if self.transitions:
            result += "transitions:" + str([str(x) + str(y) for (x,y) in self.transitions.items()])
        result += ">"
        return result

    def __bool__(self):
        return bool(self.itemlist)

    def __nonzero__(self):
        return self.__bool__()

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
        """Append new item to set"""
        if not isinstance(item, LR0Item):
            raise TypeError
        self.itemlist.append(item)

    def append_transition(self, symbol, targetset):
        """Appends a transition"""
        if symbol in self.transitions:
            return
        self.transitions[symbol] = targetset

    def has_transition(self, symbol):
        return symbol in self.transitions

    def get_transition(self, symbol):
        """gets a transition"""
        return self.transitions[symbol]

class LR0Parser(BottomUpParser):
    """LR0 bottomup parser. Not finished"""
    def __init__(self, productionset):
        #TODO: Build extended productionset before calling parent constructor
        BottomUpParser.__init__(self, productionset)
        #Add main item to itemsclosure with cursor at 0 position
        self.__parsertable = _slr_build_parser_table(productionset)
        #build GoTo and Action Table from ProductionRuleSet

    def get_trees(self, tokenlist):
        try:
            return self.__parse(tokenlist)
        except IndexError:
            return False

    def __parse(self, tokenlist):
        """see parent docstring"""
        #empty stack
        #iterate over symbollist
        if isinstance(tokenlist, str):
            tokenlist = [x for x in tokenlist]
        if not isinstance(tokenlist, list):
            raise TypeError("Expected list, got %s" % tokenlist.__class__.__name__)
        LOG.debug("get_trees: checking list: " + str(tokenlist))
        stack = [(0, Extended_S)]
        while True:
            state = stack[-1][0]
            if len(tokenlist):#FIXME: tokenlist with one element is reported as false
                token = tokenlist[0]
            else:
                token = EndSymbol()
            newdic = self.__parsertable.insert(state, token)
            action = newdic["action"]
            if action == "Fail":
                return False
            elif action == "Accept":
                return True
            if action == "Reduce":
                reductionrule = newdic["rule"]
                #TODO extract len(right side) of the rule and insert left side
                for rsymbol in reversed(reductionrule.rightside):
                    state, symbol = stack.pop() # TODO: check
                state = stack[-1][0]
                state = self.__parsertable.goto(state,reductionrule.leftside[0])
                stack.append((state, reductionrule.leftside[0]))
            elif action == "Shift":
                stack.append((newdic['dest'], tokenlist.pop(0)))
            else:
                raise ValueError("Unknown action")
        return False

