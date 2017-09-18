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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from .parser import TopDownParser
from pydsl.tree import ParseTree, PositionResultList
from pydsl.check import check


class BacktracingErrorRecursiveDescentParser(TopDownParser):
    """Recursive descent parser implementation. Backtracing. Null support. Error support"""
    def get_trees(self, data, showerrors = False): # -> list:
        """ returns a list of trees with valid guesses """
        if not all(check(self._productionset.alphabet, [x]) for x in data):
            raise ValueError("Unknown element in {}, alphabet:{}".format(str(data), self.productionset.alphabet))
        result = self.__recursive_parser(self._productionset.initialsymbol, data, self._productionset.main_production, showerrors)
        finalresult = []
        for eresult in result:
            if eresult.left == 0 and eresult.right == len(data) and eresult not in finalresult:
                finalresult.append(eresult)        
        return finalresult

    def __recursive_parser(self, onlysymbol, data, production, showerrors = False):
        """ Aux function. helps check_word"""
        LOG.debug("__recursive_parser: Begin ")
        if not data:
            return []
        from pydsl.grammar.symbol import TerminalSymbol, NullSymbol, NonTerminalSymbol
        if isinstance(onlysymbol, TerminalSymbol):
            LOG.debug("Iteration: terminalsymbol")
            return self._reduce_terminal(onlysymbol,data[0], showerrors)
        elif isinstance(onlysymbol, NullSymbol):
            return [ParseTree(0, 0, onlysymbol, "")]
        elif isinstance(onlysymbol, NonTerminalSymbol):
            validstack = []
            invalidstack = []
            for alternative in self._productionset.getProductionsBySide(onlysymbol): #Alternative
                alternativetree = PositionResultList()
                alternativeinvalidstack = []
                for symbol in alternative.rightside: # Symbol
                    symbol_success = False
                    for totalpos in alternativetree.right_limit_list(): # Right limit
                        if totalpos >= len(data):
                            continue
                        thisresult =  self.__recursive_parser(symbol, data[totalpos:], alternative, showerrors)
                        if not (thisresult and all(thisresult)):
                            alternativeinvalidstack += [x for x in thisresult if not x]
                            continue
                        symbol_success = True
                        for x in thisresult:
                            x.shift(totalpos)
                            success = alternativetree.append(x.left, x.right, x)
                            if not success:
                                #TODO: Add as an error to the tree or to another place
                                LOG.debug("Discarded symbol :" + str(symbol) + " position:" + str(totalpos))
                            else:
                                LOG.debug("Added symbol :" + str(symbol) + " position:" + str(totalpos))
                    if not symbol_success:
                        LOG.debug("Symbol doesn't work" + str(symbol))
                        break #Try next alternative
                else: # Alternative success (no break happened)
                    invalidstack += alternativeinvalidstack
                for x in alternativetree.valid_sequences():
                    validstack.append(x)
            result = []

            LOG.debug("iteration result collection finished:" + str(validstack))
            for alternative in self._productionset.getProductionsBySide(onlysymbol):
                nullcount = alternative.rightside.count(NullSymbol())
                for results in validstack:
                    nnullresults = 0
                    left = results[0]['left']
                    right = results[-1]['right']
                    nnullresults = len([x for x in results if x['content'].symbol == NullSymbol()])
                    if len(results) - nnullresults != len(alternative.rightside) - nullcount:
                        LOG.debug("Discarded: incorrect number of non null symbols")
                        continue
                    if right > len(data):
                        LOG.debug("Discarded: length mismatch")
                        continue
                    for x in range(min(len(alternative.rightside), len(results))):
                        if results[x]['content'] != alternative.rightside[x]:
                            LOG.debug("Discarded: rule doesn't match partial result")
                            continue
                    childlist = [x['content'] for x in results]
                    allvalid = all([x.valid for x in childlist])
                    if allvalid:
                        newresult = ParseTree(0, right - left, onlysymbol,
                                data[left:right], childlist = childlist)
                        newresult.valid = True
                        result.append(newresult)
            if showerrors and not result:
                erroresult = ParseTree(0,len(data), onlysymbol , data, valid = False)
                for invalid in invalidstack:
                    if invalid.content in production.rightside:
                        erroresult.append(invalid)
                return [erroresult]
            return result
        raise Exception("Unknown symbol:" + str(onlysymbol))
