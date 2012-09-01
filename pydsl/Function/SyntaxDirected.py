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



"""Syntax Directed Transformers"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from .Transformer import Transformer

class STDVarDict:
    """Stores variable-value blocks Aside rule name, each element should be
    retrievable by position in the original string"""
    def __init__(self, productionruleset):
        self.vardict = {} #store by rule name
        self.productionruleset = productionruleset

    def getInitialSymbol(self):
        """returns global dict """
        return list(self.vardict["S0"].values())[0][1]

    def getChildByNameAndBorders(self, rulename, dpr):
        thisrule = self.vardict[rulename]
        ruledpr = None
        for leftpos, rightpos in thisrule.keys():
            if leftpos >= dpr.leftpos and rightpos <= dpr.rightpos:
                ruledpr = thisrule[(leftpos, rightpos)][0]
                break
        else:
            return []
        result = []
        for unused_child in ruledpr.childlist:
            result.append((dpr.rule.name, dpr.leftpos, dpr.rightpos))
        return result

    def setByNameAndBorders(self, rulename, dpr, valuedict):
        if not rulename in self.vardict:
            self.vardict[rulename] = {}
        self.vardict[rulename][(dpr.leftpos, dpr.rightpos)] = (dpr, valuedict)

class STDCodeBlock:
    def __call__(self, vardict, rulename, dpr):
        pass

class SyntaxDirectedTransformer(Transformer):
    def __init__(self, inputgrammardic, outputgrammardic, blockdic:dict):
        assert(len(inputgrammardic) == 1)
        assert(len(outputgrammardic) == 1)
        Transformer.__init__(self, inputgrammardic, outputgrammardic, ecuid, server)
        self.blockdic = blockdic
        productionset = list(self.inputchanneldic.values())[0].productionset
        self.vardict = STDVarDict(productionset) #Donde se guardan las variables. Hay un registro general y uno por cada regla #Cada regla debe a su vez guardar una lista segun rango de la ocurrencia. Ejemplo: {"E->a+b":[(1,3)]:{"a.var":3,"b.var":5}} 

    def __parseSymbolTokenTree(self, stt, word):
        """Returns a tokenlist"""
        stts = list(self.inputchanneldic.values())[0].get_trees(word)
        assert(len(stts) == 1)
        stt = stts[0]
        #productionruleset = list(self.inputchanneldic.values())[0].productionset
        mylist = {}
        for dpr in stt.getAllByOrder():
            mylist[dpr.production.name] = dpr
        for rulename, dpr in mylist.items():
            self.blockdic[rulename](self.vardict, rulename, dpr)

    def __call__(self, worddic):
        word = list(worddic.values())[0]
        stts = list(self.inputchanneldic.values())[0].get_trees(word)
        assert(len(stts) == 1)
        stt = stts[0]
        _ = self.__parseSymbolTokenTree(stt, word)
        _ = self.blockdic["finally"](self.vardict) #El ultimo bloque que devuelve el resultado del transformador
        #return result

    @property
    def summary(self):
        inputdic = [ x.identifier for x in self.inputchanneldic.values() ]
        outputdic = [ x.identifier for x in self.outputchanneldic.values() ]
        return {"iclass":"SyntaxDirectedTransformer", "identifier":self.identifier, "input":inputdic, "output":outputdic }
