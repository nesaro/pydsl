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

"""loader class"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"
from pkg_resources import Requirement, resource_filename
from pydsl.Grammar.BNF import BNFGrammar

def load_checker(grammar):
    import re
    tmp = re.compile("a")
    if isinstance(grammar, str):
        grammar = load_grammar(grammar)
    if isinstance(grammar, BNFGrammar):
        from pydsl.Grammar.Checker import BNFChecker
        return BNFChecker(grammar)
    elif isinstance(grammar, type(tmp)):
        from pydsl.Grammar.Checker import RegularExpressionChecker
        return RegularExpressionChecker(grammar)
    elif isinstance(grammar, dict) and "matchFun" in grammar:
        from pydsl.Grammar.Checker import PythonChecker
        return PythonChecker(grammar)
    elif isinstance(grammar, dict) and "spec" in grammar:
        from pydsl.Grammar.Checker import MongoChecker
        return MongoChecker(grammar["spec"])
    else:
        raise ValueError(grammar)

def load_grammar_tool(grammar):
    from pydsl.Grammar.Tool.Python import PythonGrammarTools
    import re
    tmp = re.compile("a")
    if isinstance(grammar, str):
        grammar = load_grammar(grammar)
    if isinstance(grammar, BNFGrammar):
        from pydsl.Grammar.Tool.Symbol import SymbolGrammarTools
        return SymbolGrammarTools(grammar)
    elif isinstance(grammar, type(tmp)):
        from pydsl.Grammar.Tool.Regular import RegularExpressionGrammarTools
        return RegularExpressionGrammarTools(grammar)
    elif isinstance(grammar, dict) and "matchFun" in grammar:
        from pydsl.Grammar.Tool.Python import PythonGrammarTools
        return PythonGrammarTools(grammar)
    else:
        raise ValueError(grammar)

def load_function(identifier, memorylist = []):
    try:
        return load_board(identifier, memorylist)
    except KeyError:
        pass
    try:
        return load_transformer(identifier, memorylist)
    except KeyError:
        pass
    raise KeyError("Function" + identifier)

def load_grammar(identifier, memorylist = []):
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    for memory in memorylist:
        #if memory.provided_iclasses() and "Grammar" not in memory.provided_iclasses():
        #    continue
        if identifier in memory:
            return memory.load(identifier)
    raise KeyError("Grammar " + identifier)

def load_transformer(identifier, memorylist = []):
    #FIXME: Can return any type of element
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist

    for memory in memorylist:
        if identifier in memory:
            return memory.load(identifier)
    raise KeyError("Transformer: " + identifier)

def load_board(identifier, memorylist = []):
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    for memory in memorylist:
        if "Board" not in memory.provided_iclasses():
            continue
        if identifier in memory:
            return memory.load(identifier)
    raise KeyError("Board" + identifier)
