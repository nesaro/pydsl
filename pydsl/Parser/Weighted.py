#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2013 Nestor Arocha
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
from .Parser import TopDownParser, terminal_symbol_reducer
from pydsl.Tree import ParseTree

def filter_by_size(l, size):
    for element in l[:]:
        if len(element) != size:
            l.remove(element)
    return l

def _create_combined_list(input_list):
    """
    Creates a list of lists, each sublist contains a permutation of inputs. E.g:
    [a, b, c] -> [[a1,b1,c1],[a2,b1,c1]] ....
    """

    input_list = [x for x in input_list if x]
    if not input_list:
        return []

    # All blocks combinations are stored here.
    # Each element is a list of viable sequences
    midlist = [[x] for x in input_list[0] if not x.leftpos]

    valid_sets = 1
    #Processing Tail sets
    for group in input_list[1:]:
        #For each result list
        if not group:
            continue
        for result in group:
            #for each result
            for existing_result in midlist[:]:
                #Here we mix every result with intermediate results list
                prev_right = [x.rightpos for x in existing_result if x.rightpos is not None][-1]
                if result.leftpos is None or prev_right == result.leftpos:
                    midlist.append(existing_result + [result])
        valid_sets += 1

        #Removes all results that have less elements than the number of valid sets
        midlist = filter_by_size(midlist, valid_sets)
    return midlist

def mix_results(resultll, productionset):
    """ Mix n sets of results """
    #We mix all results into final result
    midlist = _create_combined_list(resultll)
    finallist = []
    for combination in midlist:
        if len(combination) == 1:
            finallist.append(combination[0])
            continue
        left_pos = [x.leftpos for x in combination if x.leftpos is not None][0]
        right_pos = [x.rightpos for x in combination if x.rightpos is not None][-1]
        compoundword = "".join([str(x.content) for x in combination])
        #Creates a node with all elements, and originals nodes are the childs of the new node
        symbollist = []
        for element in combination:
            if isinstance(element.symbol, list):
                symbollist += element.symbol
            else:
                symbollist.append(element.symbol)
        finalresult = ParseTree(left_pos, right_pos, symbollist, compoundword, valid = all([x for x in combination]))
        #Add childs to result. FIXME Adding already created elements as children of the new one
        rightside = []
        for child in combination:
            assert(child != finalresult) #Avoid recursion
            finalresult.append_child(child)
            if isinstance(child.symbol, list):
                rightside += child.symbol #Creating the rightside of the production to guess the full production #FIXME doesn't work with terminals
            else:
                rightside.append(child.symbol)
        try:
            finalresult.production = productionset.getProductionsBySide(rightside, "right")
        except IndexError:
            finalresult.production = None
        finally:
            finallist.append(finalresult) #rule found; we add bound together version
    return finallist

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
        result = self.__recursive_parser(self._productionset.initialsymbol, data, self._productionset.main_production, showerrors)
        finalresult = []
        for eresult in result:
            if eresult.leftpos == 0 and eresult.rightpos == len(data):
                finalresult.append(eresult)
        return finalresult

    def __handle_alternative(self,symbols, data, production, showerrors):
        """Multiple symbols
        returns a list of possible reductions"""
        if len(symbols) == 1:
            return self.__recursive_parser(symbols[0], data, production, showerrors)
        heavy_symbol = locate_heavier_symbol(symbols)
        index = symbols.index(heavy_symbol)
        LOG.debug("Iteration: Call recursive heavy" + str(heavy_symbol) + str(index))
        heavyresult = self.__recursive_parser(heavy_symbol, data, production, showerrors)
        if not heavyresult:
            return []
        leftpos = max([x.leftpos for x in heavyresult])
        rightpos = min([x.rightpos for x in heavyresult]) or 0
        leftside = []
        rightside = []
        if symbols[:index]:
            LOG.debug("Iteration: Call recursive left")
            leftside = self.__handle_alternative(symbols[:index], data[:leftpos], production, showerrors)
        if symbols[(index+1):]:
            LOG.debug("Iteration: Call recursive right")
            rightside = self.__handle_alternative(symbols[(index+1):], data[rightpos:], production, showerrors)
            #shift right results
        for x in rightside:
            x.shift(rightpos)
        if not leftside and not rightside:
            return heavyresult
        result = mix_results([leftside, heavyresult, rightside], self._productionset)
        return result

    def __recursive_parser(self, onlysymbol, data, production, showerrors = False):
        """ Main function. It is recursive """
        from pydsl.Grammar.Symbol import TerminalSymbol, NonTerminalSymbol, NullSymbol
        if isinstance(onlysymbol, TerminalSymbol):
            #Locate every occurrence of word and return a set of results. Follow boundariesrules
            LOG.debug("Iteration: terminalsymbol")
            result = terminal_symbol_reducer(onlysymbol, data, onlysymbol)
            if showerrors and not result:
                return [ParseTree(0,len(data), onlysymbol , data, valid = False)]
            return result
        elif isinstance(onlysymbol, NonTerminalSymbol):
            result = []
            for alternative in self._productionset.getProductionsBySide(onlysymbol):
                #result += self.__recursive_parser(alternative.rightside, data, alternative, showerrors)
                alternative_result = self.__handle_alternative(alternative.rightside, data, alternative, showerrors)
                for x in alternative_result:
                    x_symbol = x.symbol
                    if not isinstance(x_symbol, list):
                        x_symbol = [x_symbol]
                    if x_symbol == list(alternative.rightside): #Filters incomplete attempts
                        result.append(ParseTree(x.leftpos, x.rightpos, onlysymbol, data[x.leftpos:x.rightpos], valid = True))
                    #TODO: Add child
            if showerrors and not result:
                return [ParseTree(0, len(data), onlysymbol, data, valid = False)]
            LOG.debug("Result " + str(result))
            return result
        elif isinstance(onlysymbol, NullSymbol):
            return[ParseTree(None, None, onlysymbol, "")]
        raise Exception
