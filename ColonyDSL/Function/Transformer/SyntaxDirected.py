#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Nestor Arocha Rodríguez

"""Syntax Directed Transformers"""

import logging
LOG = logging.getLogger("SyntaxDirectedTransformer")
from .Transformer import Transformer

class STDVarDict:
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
        if not ruledpr:
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
    def __init__(self, inputgrammardic, outputgrammardic, blockdic:dict, ecuid = None, server = None):
        assert(len(inputgrammardic) == 1)
        assert(len(outputgrammardic) == 1)
        Transformer.__init__(self, inputgrammardic, outputgrammardic, ecuid, server)
        self.blockdic = blockdic
        productionset = list(self.inputchanneldic.values())[0].productionset
        self.vardict = STDVarDict(productionset) 

    def __parseSymbolTokenTree(self, stt, word):
        stts = list(self.inputchanneldic.values())[0].get_trees(word)
        assert(len(stts) == 1)
        stt = stts[0]
        mylist = {}
        for dpr in stt.getAllByOrder():
            mylist[dpr.production.name] = dpr
        for rulename, dpr in mylist.items():
            self.blockdic[rulename](self.vardict, rulename, dpr)

    def _onReceiveEvent(self, source, msg):
        pass

    def __call__(self, worddic):
        word = list(worddic.values())[0]
        stts = list(self.inputchanneldic.values())[0].get_trees(word)
        assert(len(stts) == 1)
        stt = stts[0]
        _ = self.__parseSymbolTokenTree(stt, word)
        _ = self.blockdic["finally"](self.vardict) 
        #return result

    @property
    def summary(self):
        inputdic = [ x.identifier for x in self.inputchanneldic.values() ]
        outputdic = [ x.identifier for x in self.outputchanneldic.values() ]
        return {"iclass":"SyntaxDirectedTransformer", "identifier":self.identifier, "description":self.description, "input":inputdic, "output":outputdic }
