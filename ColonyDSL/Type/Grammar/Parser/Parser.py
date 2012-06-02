#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Néstor Arocha Rodríguez

"""Parser module"""

import logging
LOG = logging.getLogger("Parser")
from abc import ABCMeta, abstractmethod
from ColonyDSL.Abstract import TypeCheckList


def terminal_symbol_reducer(symbol, word, production):
    """ Reduces a terminal symbol """
    from ColonyDSL.Abstract import TypeCheckList
    from ColonyDSL.Type.Grammar.Tree import ParseTree
    if not isinstance(word, str):
        word = str(word)
    validresults = TypeCheckList(ParseTree)
    if symbol.boundariesrules.policy == "min":
        LOG.debug("terminal_symbol_reducer: policy: min")
        for begin in range(0, len(word)):
            for end in range(begin, len(word)+1):
                if symbol.check(word[begin:end]):
                    LOG.debug("terminal_symbol_reducer: parsed:"+ str(word[begin:end]))
                    validresults.append(ParseTree(begin, end, [symbol], word[begin:end], production))
                    break #found the smallest valid symbol at begin
    elif symbol.boundariesrules.policy == "max":
        LOG.debug("terminal_symbol_reducer: policy: max")
        for begin in range(0, len(word)):
            maxword = 0
            for end in range(begin, len(word)+1):
                if symbol.check(word[begin:end]):
                    LOG.debug("terminal_symbol_reducer: parsed:"+ str(word[begin:end]))
                    maxword = end
            if maxword > 0:
                validresults.append(ParseTree(begin, maxword, [symbol], word[begin:maxword], production))
    elif symbol.boundariesrules.policy == "fixed":
        LOG.debug("terminal_symbol_reducer: policy: fixed")
        size = symbol.boundariesrules.size
        for begin in range(0, len(word)):
            if symbol.check(word[begin:begin + size]):
                LOG.debug("__auxReducer: parsed:"+ str(word[begin:begin + size]))
                validresults.append(ParseTree(begin, begin + size, [symbol], word[begin:begin + size], production))
    else:
        LOG.warning("terminal_symbol_reducer: Unknown size policy")
        return TypeCheckList(ParseTree)
    return validresults

def terminal_symbol_consume(symbol, word, production):
    """ Reduces a terminal symbol. Always start from left"""
    from ColonyDSL.Abstract import TypeCheckList
    from ColonyDSL.Type.Grammar.Tree import ParseTree
    validresults = TypeCheckList(ParseTree)
    begin = 0
    if symbol.boundariesrules.policy == "min":
        for end in range(begin, len(word)+1):
            if symbol.check(word[begin:end]):
                return [ParseTree(begin, end, [symbol], word[begin:end], production)]
    elif symbol.boundariesrules.policy == "max":
        LOG.debug("terminal_symbol_reducer: policy: max")
        maxword = 0
        for end in range(begin, len(word)+1):
            if symbol.check(word[begin:end]):
                LOG.debug("terminal_symbol_reducer: parsed:"+ str(word[begin:end]))
                maxword = end
        if maxword > 0:
           return[ParseTree(begin, maxword, [symbol], word[begin:maxword], production)]
    elif symbol.boundariesrules.policy == "fixed":
        size = symbol.boundariesrules.size
        LOG.debug("terminal_symbol_reducer: policy: fixed " + str(size))
        if len(word) >= size and symbol.check(word[:size]):
            return [ParseTree(0, size, [symbol], word[:size], production)]
    else:
        LOG.warning("terminal_symbol_reducer: Unknown size policy")
        return TypeCheckList(ParseTree)
    return validresults

def mix_results(resultll:list, productionset):
    """ Mix n sets of results """
    from ColonyDSL.Type.Grammar.Tree import ParseTree
    production = None
    for resultl in resultll:
        assert(isinstance(resultl, TypeCheckList) and resultl.instancetype == ParseTree)
    midlist = [] #All blocks combinations are stored here
    firstindex = 0
    while firstindex < len(resultll) and len(resultll[firstindex]) == 0: 
        firstindex += 1
    if firstindex == len(resultll):
        return []
    validsets = 1

    #Processing head set

    firstresultl = resultll[firstindex]
    for result in firstresultl:
        if not(isinstance(result, ParseTree)):
            raise TypeError
        if result.leftpos == 0:
            midlist.append([result])
        elif result.leftpos == None:
            raise Exception #FIXME:What's the right thing to do here? 

    #Processing Tail sets
    for resultl in resultll[firstindex + 1:]:
        #For each result list
        if len(resultl) == 0:
            continue
        for result in resultl:
            #for each result
            tmp = []
            for middleresult in midlist:
                #combinamos todos los elementos con los ya apuntados en la lista intermedia
                #Here we mix every result with intermediate results list
                lastresult = middleresult[-1]
                if lastresult.production != result.production:
                    pass
                if result.rightpos == None:
                    result.rightpos = lastresult.rightpos
                    result.leftpos = lastresult.rightpos
                if lastresult.rightpos == None or result.leftpos == None:
                    tmp.append(middleresult + [ParseTree(result.leftpos, result.rightpos, \
                            result.symbollist, result.content, result.production, \
                            TypeCheckList(ParseTree, result.childlist), result.valid)])
                elif lastresult.rightpos == result.leftpos:
                    tmp.append(middleresult + [ParseTree(result.leftpos, result.rightpos, \
                            result.symbollist, result.content, result.production, \
                            TypeCheckList(ParseTree, result.childlist), result.valid)])
            midlist += tmp
        validsets += 1
    
        #eliminamos los resultados intermedios que no contienen tantos elementos como hemos procesado. Es decir, no se ha encontrado una combinacion valida en la ultima mezcla
        #Removes all results that have less elements than the number of valid sets
        for element in midlist[:]:
            if len(element) != validsets:
                midlist.remove(element)

    #Combinamos resultados en la lista final
    #We mix all results into final result
    finallist = TypeCheckList(ParseTree)
    for middleresult in midlist:
        if len(middleresult) == 1:
            finallist.append(middleresult[0])
        elif middleresult[0].leftpos != None and middleresult[-1].rightpos != None:
            #mezclamos la coleccion y dejamos los originales como hijos
            #Creates a node with all elements, and originals nodes are the childs of the new node
            symbollist = []
            for element in middleresult:
                compoundword += element.content
                symbollist += element.symbollist
            finalresult = ParseTree(middleresult[0].leftpos, middleresult[-1].rightpos, symbollist, compoundword, middleresult[0].production, valid = result.valid)
            psl = middleresult[0].production
            #Add childs to result. FIXME El problema es que estamos añadiendo como hijos del nuevo los elementos ya creados
            error = False
            rightside = []
            for child in middleresult:
                assert(child != finalresult)
                finalresult.append_child(child)
                if child.production:
                    rightside += child.production.leftside
                if not child.valid:
                    finalresult.valid = False #valid status propagates upwards
            #if error:
            #    print([str(x.production) for x in middleresult])
            #    continue
            if productionset:
                try:
                    finalresult.production = productionset.getProductionsBySide(rightside, "right")
                except IndexError:
                    finallist += middleresult #rule not found: we add it unprocessed (non joined version)
                else:
                    finallist.append(finalresult) #rule found; we add binded together version
        else:
            raise Exception
    return finallist

def locate_result_borders(results):
    """ Finds the most conservative borders values"""
    leftborder = 0
    rightborder = 10**10
    for result in results:
        leftpos = result.leftpos
        rightpos = result.rightpos
        if leftpos == None and rightpos == None:
            return (rightborder, leftborder)
        if leftpos > leftborder:
            leftborder = leftpos
        if rightpos < rightborder:
            rightborder = rightpos
    return (leftborder, rightborder)

class Parser(metaclass = ABCMeta):
    """Parser abstract class. At this time, all parsers are tree based"""
    from .Production import ProductionSet
    def __init__(self, productionruleset:ProductionSet):
        self._productionset = productionruleset

    @abstractmethod
    def check(self, word):
        """ Checks if word is valid for current productionruleset """
        pass

    @abstractmethod
    def get_trees(self, word) -> list:
        """ returns a SymbolTokenTree with all guesses """
        pass

    @property
    def productionset(self):
        """returns productionset"""
        return self._productionset

    #@abstractproperty
    def alphabet(self):
        return set()

    def enumerate(self):
        return set()

class TopDownParser(Parser):
    """Top down parser like descent parser"""
    def check(self, word):
        """ Checks if word is valid for current productionruleset """
        return len(self.get_trees(word)) > 0
        
class BottomUpParser(Parser):
    """ leaf to root parser"""
    def __init__(self, productionruleset, packagedependencies = None):
        terminalsymbollist = productionruleset.getTerminalSymbols()
        for ts in terminalsymbollist:
            from ColonyDSL.Type.Grammar.Symbol import WordTerminalSymbol
            if isinstance(ts, WordTerminalSymbol):
                LOG.critical("BottomUp parsers can't handle WordTerminalSymbol yet")
                raise Exception
        Parser.__init__(self, productionruleset)
        
    @abstractmethod
    def _symbolize_word(self, word):
        """Convert input word into symbols"""
        #parse wordtokens
        #search for chartokens that belongs to wordsymbols
        #assing else to charsymbols
        pass

