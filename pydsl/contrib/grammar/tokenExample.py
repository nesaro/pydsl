#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2013 Nestor Arocha

"""
Token example grammar.   
accepts only "1+1"
"""

from pydsl.Grammar.Symbol import StringTerminalSymbol as _CTS, WordTerminalSymbol as _WTS, NonTerminalSymbol as _NTS, BoundariesRules as _BR
from pydsl.Grammar.BNF import Production as _NTP

_br = _BR("max", 1)


_symbol1 = _WTS("one", {"grammarname":"integer"}, _br)
_symbol2 = _CTS("+")
initialsymbol = _NTS("exp") 

_rule1 = _NTP([initialsymbol], [_symbol1, _symbol2, _symbol1])
fulllist = [_rule1, _symbol1, _symbol2]
iclass = "SymbolGrammar"
