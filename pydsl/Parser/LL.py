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

"""LL family parsers"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"
from pydsl.Check import check
from pydsl.Parser.Parser import TopDownParser
from pydsl.Tree import ParseTree
import logging
LOG = logging.getLogger(__name__)



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
