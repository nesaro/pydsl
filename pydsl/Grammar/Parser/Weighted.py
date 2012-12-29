#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Nestor Arocha
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

"""WeightedParser"""

import logging
LOG = logging.getLogger(__name__)
from .Parser import TopDownParser, mix_results, locate_result_borders, terminal_symbol_reducer
from ..Tree import ParseTree

def locate_heavier_symbol(symbols):
    """ Locates the heavier symbol inside input list"""
    current_symbol = None
    for symbol in symbols:
        if current_symbol is None or symbol.weight > current_symbol.weight:
            current_symbol = symbol
    return current_symbol

class WeightedParser(TopDownParser):
    """Weighted Parser class"""
    def get_trees(self, data, showerrors = False):
        """See parent definition"""
        result = self.__recursive_parser([self._productionset.initialsymbol], data, self._productionset.main_production, showerrors)
        finalresult = []
        for eresult in result:
            if eresult.leftpos == 0 and eresult.rightpos == len(data):
                finalresult.append(eresult)
        return finalresult

    def __recursive_parser(self, symbols, data, production, showerrors = False):
        """ Main function. It is recursive """
        if not symbols:
            return []
        if len(symbols) > 1:
            currentsymbol = locate_heavier_symbol(symbols)
            index = symbols.index(currentsymbol)
            LOG.debug("Iteration: Call recursive heavy")
            heavyresult = self.__recursive_parser([currentsymbol], data, production, showerrors)
            if not heavyresult:
                return []
            leftpos, rightpos = locate_result_borders(heavyresult)
            leftside = []
            rightside = []
            if index > 0:
                LOG.debug("Iteration: Call recursive left")
                leftside = self.__recursive_parser(symbols[:index], data[:leftpos], production, showerrors)
                if not leftside:
                    return []
            LOG.debug("Iteration: Call recursive right")
            if (index + 1) < len(symbols):
                rightside = self.__recursive_parser(symbols[(index+1):], data[rightpos:], production, showerrors)
                if not rightside:
                    return []
            #shift right results
            for rsresult in rightside:
                rsresult.shift(rightpos)
            result = mix_results([leftside, heavyresult, rightside], self._productionset) 
            return result
        onlysymbol = symbols[0]
        from ..Symbol import TerminalSymbol, NonTerminalSymbol, NullSymbol
        if isinstance(onlysymbol, TerminalSymbol):
            #Locate every occurrence of word and return a set of results. Follow boundariesrules
            LOG.debug("Iteration: terminalsymbol")
            result =  terminal_symbol_reducer(onlysymbol, data, None) #FIXME add information about production
            if showerrors and not result:
                return [ParseTree(0,len(data), [onlysymbol] , data, None, valid = False)] #FIXME add information about production
            return result
        elif isinstance(onlysymbol, NonTerminalSymbol):
            result = []
            for alternative in self._productionset.getProductionsBySide([onlysymbol]):
                result += self.__recursive_parser(alternative.rightside, data, alternative, showerrors)
            if showerrors and not result:
                return [ParseTree(0, len(data), [onlysymbol], data, production, valid = False)]
            return result
        elif isinstance(onlysymbol, NullSymbol):
            return[ParseTree(None, None, [onlysymbol], "", production)]
        raise Exception
