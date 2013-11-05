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

"""Recursive descent parser"""
from pydsl import Tree
from pydsl.Check import check

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from .Parser import TopDownParser, terminal_symbol_reducer
from pydsl.Tree import ParseTree, Tree, Sequence

class BacktracingErrorRecursiveDescentParser(TopDownParser):
    """Recursive descent parser implementation. Backtracing. Null support. Error support"""
    def get_trees(self, data, showerrors = False): # -> list:
        """ returns a list of trees with valid guesses """
        result = self.__recursive_parser(self._productionset.initialsymbol, data, self._productionset.main_production, showerrors)
        finalresult = []
        for eresult in result:
            if eresult.leftpos == 0 and eresult.rightpos == len(data) and eresult not in finalresult:
                finalresult.append(eresult)        
        return finalresult

    def __recursive_parser(self, onlysymbol, data, production, showerrors = False):
        """ Aux function. helps check_word"""
        LOG.debug("__recursive_parser: Begin ")
        if not data:
            return []
        from pydsl.Grammar.Symbol import TerminalSymbol, NullSymbol, NonTerminalSymbol
        if isinstance(onlysymbol, TerminalSymbol):
            #Locate every occurrence of word and return a set of results. Follow boundariesrules
            LOG.debug("Iteration: terminalsymbol")
            result = terminal_symbol_reducer(onlysymbol, data, production, fixed_start=True)
            if showerrors and not result:
                return [ParseTree(0,len(data), [onlysymbol] , data, onlysymbol, valid = False)]
            return result
        elif isinstance(onlysymbol, NullSymbol):
            return [ParseTree(0, 0, [onlysymbol], "", production)]
        elif isinstance(onlysymbol, NonTerminalSymbol):
            validstack = []
            invalidstack = []
            for alternative in self._productionset.getProductionsBySide([onlysymbol]): #Alternative
                alternativetree = Sequence()
                alternativeinvalidstack = []
                for symbol in alternative.rightside: # Symbol
                    symbol_success = False
                    for totalpos in alternativetree.right_limit_list(): # Right limit
                        if totalpos >= len(data):
                            continue
                        thisresult =  self.__recursive_parser(symbol, data[totalpos:], alternative, showerrors)
                        if thisresult and all(thisresult):
                            symbol_success = True
                            for x in thisresult:
                                x.shift(totalpos)
                                success = alternativetree.append(x.leftpos, x.rightpos, x)
                                if not success:
                                    #TODO: Add as an error to the tree or to another place
                                    LOG.debug("Discarded symbol :" + str(symbol) + " position:" + str(totalpos))
                                else:
                                    LOG.debug("Added symbol :" + str(symbol) + " position:" + str(totalpos))
                        else:
                            alternativeinvalidstack += [x for x in thisresult if not x]

                    if not symbol_success:
                        LOG.debug("Symbol doesn't work" + str(symbol))
                        break #Try next alternative
                else: # Alternative success (no break happened)
                    invalidstack += alternativeinvalidstack
                for x in alternativetree.generate_valid_sequences():
                    validstack.append(x)
            result = []

            LOG.debug("iteration result collection finished:" + str(validstack))
            for alternative in self._productionset.getProductionsBySide([onlysymbol]):
                nullcount = alternative.rightside.count(NullSymbol())
                for results in validstack:
                    nnullresults = 0
                    leftpos = results[0]['left']
                    rightpos = results[-1]['right']
                    for y in [x['content'].symbollist for x in results]:
                        nnullresults += y.count(NullSymbol())
                    if len(results) - nnullresults != len(alternative.rightside) - nullcount:
                        LOG.debug("Discarded: incorrect number of non null symbols")
                        continue
                    if rightpos > len(data):
                        LOG.debug("Discarded: length mismatch")
                        continue
                    for x in range(min(len(alternative.rightside), len(results))):
                        if results[x]['content'] != alternative.rightside[x]:
                            LOG.debug("Discarded: rule doesn't match partial result")
                            continue
                    childlist = [x['content'] for x in results]
                    allvalid = all([x.valid for x in childlist])
                    if allvalid:
                        newresult = ParseTree(0, rightpos - leftpos, [onlysymbol],
                                data[leftpos:rightpos], alternative, childlist)
                        newresult.valid = True
                        result.append(newresult)
            if showerrors and not result:
                erroresult = ParseTree(0,len(data), [onlysymbol] , data, production, valid = False)
                for invalid in invalidstack:
                    current_symbol = invalid.production if isinstance(invalid.production, (TerminalSymbol, NullSymbol)) else invalid.production.leftside[0]
                    if current_symbol in production.rightside:
                        erroresult.append_child(invalid)
                return [erroresult]
            return result
        raise Exception("Unknown symbol:" + str(onlysymbol))

class BacktracingRecursiveDescentParser(TopDownParser):
    """Recursive descent parser implementation. Backtracing"""
    def get_trees(self, data, showerrors = False): # -> list:
        """ returns a list of trees with valid guesses """
        if showerrors:
            raise NotImplementedError("This parser doesn't implement errors")
        result = self.__recursive_parser(self._productionset.initialsymbol, data, self._productionset.main_production)
        finalresult = []
        for eresult in result:
            if eresult.leftpos == 0 and eresult.rightpos == len(data) and eresult not in finalresult:
                finalresult.append(eresult)        
        return finalresult

    def __recursive_parser(self, onlysymbol, data, production):
        """ Aux function. helps check_word"""
        LOG.debug("__recursive_parser: Begin ")
        if not data:
            return []
        from pydsl.Grammar.Symbol import TerminalSymbol, NonTerminalSymbol
        if isinstance(onlysymbol, TerminalSymbol):
            #Locate every occurrence of word and return a set of results. Follow boundariesrules
            LOG.debug("Iteration: terminalsymbol")
            result = terminal_symbol_reducer(onlysymbol, data, production, fixed_start=True)
            return result
        elif isinstance(onlysymbol, NonTerminalSymbol):
            validstack = []
            for alternative in self._productionset.getProductionsBySide([onlysymbol]): #Alternative
                alternativetree = Sequence()
                for symbol in alternative.rightside: # Symbol
                    symbol_success = False
                    for totalpos in alternativetree.right_limit_list(): # Right limit
                        if totalpos >= len(data):
                            continue
                        thisresult =  self.__recursive_parser(symbol, data[totalpos:], alternative)
                        if thisresult and all(thisresult):
                            symbol_success = True
                            for x in thisresult:
                                x.shift(totalpos)
                                alternativetree.append(x.leftpos, x.rightpos, x)
                    if not symbol_success:
                        LOG.debug("Symbol doesn't work" + str(symbol))
                        break #Try next alternative
                for x in alternativetree.generate_valid_sequences():
                    validstack.append(x)
            result = []

            LOG.debug("iteration result collection finished:" + str(validstack))
            for alternative in self._productionset.getProductionsBySide([onlysymbol]):
                for results in validstack:
                    leftpos = results[0]['left']
                    rightpos = results[-1]['right']
                    if len(results) != len(alternative.rightside): 
                        LOG.debug("Discarded: incorrect number of non null symbols")
                        continue
                    if rightpos > len(data):
                        LOG.debug("Discarded: length mismatch")
                        continue
                    for x in range(min(len(alternative.rightside), len(results))):
                        if results[x]['content'] != alternative.rightside[x]:
                            LOG.debug("Discarded: rule doesn't match partial result")
                            continue
                    childlist = [x for x in results]
                    newresult = ParseTree(0, rightpos - leftpos, [onlysymbol],
                            data[leftpos:rightpos], alternative, childlist)
                    newresult.valid = True
                    result.append(newresult)
            return result
        raise Exception("Unknown symbol:" + str(onlysymbol))

class LL1RecursiveDescentParser(TopDownParser):
    def get_trees(self, data, showerrors = False): # -> list:
        """ returns a list of trees with valid guesses """
        if showerrors:
            raise NotImplementedError("This parser doesn't implement errors")
        self.data = data
        self.index = 0
        try:
            return [self.__aux_parser(self._productionset.initialsymbol)]
        except IndexError:
            return []

    def __aux_parser(self, symbol):
        from pydsl.Grammar.Symbol import TerminalSymbol
        if isinstance(symbol, TerminalSymbol):
            LOG.debug("matching symbol %s, data:%s, index:%s" % (symbol,self.data,self.index ))
            result= self.match(symbol)
            LOG.debug("symbol matched %s" % result)
            return result
        productions = self._productionset.getProductionsBySide(symbol)
        valid_firsts = []        
        for production in productions:
            first_of_production = self._productionset.first_lookup(production.rightside[0])
            if check(first_of_production, self.current):
                valid_firsts.append(production)
        if len(valid_firsts) != 1:
            raise Exception("Expected only one valid production, found %s" % len(valid_firsts))
        childlist = []
        for element in valid_firsts[0].rightside:
            childlist.append(self.__aux_parser(element))
        left = childlist[0].leftpos
        right = childlist[-1].rightpos
        content = [x.content for x in childlist]
        return ParseTree(left, right, [symbol], content, valid_firsts[0], childlist=childlist)


    def consume(self):
        self.index +=1
        if self.index > len(self.data):
            raise IndexError("Attempted to consume index %s of data %s" % (self.index, self.data))

    @property
    def current(self):
        result = self.data[self.index]
        return result

    def match(self, symbol):
        if symbol.check(self.current):
            current = self.current
            self.consume()
            return ParseTree(self.index-1, self.index, [symbol], current, None)
        else:
            raise Exception("Not matched")


class LLkRecursiveDescentParser(TopDownParser):
    def get_trees(self, data, lookahead=1, showerrors = False): # -> list:
        """ returns a list of trees with valid guesses """
        if showerrors:
            raise NotImplementedError("This parser doesn't implement errors")
        self.data = data
        self.index = 0
        self.lookahead=lookahead
        return [self.__aux_parser(self._productionset.initialsymbol)]

    def __aux_parser(self, symbol):
        from pydsl.Grammar.Symbol import TerminalSymbol
        if isinstance(symbol, TerminalSymbol):
            LOG.debug("matching symbol %s, data:%s, index:%s" % (symbol,self.data,self.index ))
            result= self.match(symbol)
            LOG.debug("symbol matched %s" % result)
            return result
        valid_firsts = []
        productions = self._productionset.getProductionsBySide(symbol)
        for production in productions:
            first_of_production = self._productionset.first_lookup(production.rightside[0])
            if check(first_of_production, self.current):
                valid_firsts.append(production)
        if len(valid_firsts) != 1:
            raise Exception("Expected only one valid production, found %s" % len(valid_firsts))
        childlist = []
        for element in valid_firsts[0].rightside:
            childlist.append(self.__aux_parser(element))
        left = childlist[0].leftpos
        right = childlist[-1].rightpos
        content = [x.content for x in childlist]
        return ParseTree(left, right, [symbol], content, valid_firsts[0], childlist=childlist)


    def consume(self):
        self.index +=1
        if self.index > len(self.data):
            raise IndexError("Attempted to consume index %s of data %s" % (self.index, self.data))

    @property
    def current(self):
        result = self.data[self.index]
        return result

    def match(self, symbol):
        if symbol.check(self.current):
            current = self.current
            self.consume()
            return ParseTree(self.index-1, self.index, [symbol], current, None)
        else:
            raise Exception("Not matched")

