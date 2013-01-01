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
from .Parser import TopDownParser, locate_result_borders, terminal_symbol_reducer
from pydsl.Grammar.Tree import ParseTree


def _create_combined_list(resultll):
    """
    Creates a list of lists, each sublist contains a permutation of inputs. E.g:
    [a, b, c] -> [[a1,b1,c1],[a2,b1,c1]] ....
    """

    if len(resultll) != 3:
        raise ValueError

    midlist = [] #All blocks combinations are stored here. Each element is a list of viable sequences
    resultll = [x for x in resultll if x]
    if not resultll:
        return []
    validsets = 1

    #Processing head set

    for result in resultll[0]:
        if not(isinstance(result, ParseTree)):
            raise TypeError
        if result.leftpos == 0:
            midlist.append([result])
        elif result.leftpos is None:
            raise Exception #FIXME:What's the right thing to do here?

    #Processing Tail sets
    for resultl in resultll[1:]:
        #For each result list
        if not resultl:
            continue
        for result in resultl:
            #for each result
            tmp = []
            for middleresult in midlist:
                #Here we mix every result with intermediate results list
                lastresult = middleresult[-1]
                if result.rightpos is None: #NullSymbol
                    result.rightpos = lastresult.rightpos
                    result.leftpos = lastresult.rightpos
                if (lastresult.rightpos is None or result.leftpos is None) or lastresult.rightpos == result.leftpos:
                    tmp.append(middleresult + [ParseTree(result.leftpos, result.rightpos,
                        result.symbollist, result.content, result.production,
                        list(result.childlist), result.valid)])
            midlist += tmp
        validsets += 1

        #Removes all results that have less elements than the number of valid sets
        for element in midlist[:]:
            if len(element) != validsets:
                midlist.remove(element)

    return midlist

def mix_results(resultll, productionset):
    """ Mix n sets of results """
    #We mix all results into final result
    midlist = _create_combined_list(resultll)
    finallist = []
    for combination in midlist:
        if len(combination) == 1:
            finallist.append(combination[0])
        elif combination[0].leftpos != None and combination[-1].rightpos != None:
            #Creates a node with all elements, and originals nodes are the childs of the new node
            symbollist = []
            compoundword = ""
            for element in combination:
                compoundword += element.content
                symbollist += element.symbollist
            finalresult = ParseTree(combination[0].leftpos, combination[-1].rightpos, symbollist, compoundword, combination[0].production, valid = all([x for x in combination]))
            #Add childs to result. FIXME El problema es que estamos añadiendo como hijos del nuevo los elementos ya creados
            rightside = []
            for child in combination:
                assert(child != finalresult) #Avoid recursion
                finalresult.append_child(child)
                assert(len(child.symbollist) == 1)
                rightside += child.symbollist #Creating the rightside of the production to guess the full production #FIXME doesn't work with terminals
            try:
                finalresult.production = productionset.getProductionsBySide(rightside, "right")
            except IndexError:
                pass
            else:
                finallist.append(finalresult) #rule found; we add binded together version
        else:
            raise Exception
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
