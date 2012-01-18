#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2011 Néstor Arocha Rodríguez

"""Python Function Grammar"""

from .Grammar import Grammar
import logging
LOG = logging.getLogger("Grammar.Python")

class PythonGrammar(Grammar):
    def __init__(self, identifier, matchFun, propFun = None, enumFun = None, alphabetFun = None):
        Grammar.__init__(self, identifier)
        self._matchFun = matchFun
        self._askprop = propFun
        self._enumFun = enumFun
        self._alphabetFun = alphabetFun

    def check(self, word):
        from .Result import DiscreteGrammarResult
        if not self._matchFun:
            return DiscreteGrammarResult(False) #Match function isn't defined
        try:
            return DiscreteGrammarResult(self._matchFun(word))
        except UnicodeDecodeError:
            return DiscreteGrammarResult(False)

    def get_groups(self, word, propertyname):
        if self._askprop != None:
            return [self._askprop(word, propertyname)]
        return []

    def enumerate(self):
        if self._enumFun != None:
            return set(self._enumFun())
        return set()

    @property
    def alphabet(self) -> set:
        if self._alphabetFun != None:
            return set(self._alphabetFun())
        return set()

    @property
    def summary(self):
        return {"iclass":"PythonGrammar", "identifier":self.identifier, "ancestors":self.ancestors() }

class HostPythonGrammar(PythonGrammar):
    def __init__(self, identifier, matchFun, auxdic, propFun = None):
        PythonGrammar.__init__(self, identifier, matchFun, propFun)
        self.auxgrammar = {}
        from ColonyDSL.Memory.External.Loader import load_grammar
        for key, value in auxdic.items():
            self.auxgrammar[key] = load_grammar(value)

    def check(self, word):
        from .Result import DiscreteGrammarResult
        if not self._matchFun:
            return DiscreteGrammarResult(False) #Match function isn't defined
        try:
            return DiscreteGrammarResult(self._matchFun(word, self.auxgrammar))            
        except UnicodeDecodeError:
            LOG.exception("Unicode Error while calling matchfun")
            return DiscreteGrammarResult(False)
        

