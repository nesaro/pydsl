#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of ColonyDSL.
#
#ColonyDSL is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#ColonyDSL is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with ColonyDSL.  If not, see <http://www.gnu.org/licenses/>.

"""Types FileLibraries"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


import logging
LOG = logging.getLogger("Storage.Directory.Type")
from ColonyDSL.Type.Grammar.Symbol import SymbolGrammar
from .DirStorage import DirStorage, getFileTuple

def _isGDLFileName(path):
    return path.endswith(".bnf")

def _isRELFileName(path):
    return path.endswith(".re")

def _loadRELGrammarFromFile(filepath):
    from ColonyDSL.Memory.Storage.Directory.Regexp import colonyRELfileToGrammarInstance
    instance = colonyRELfileToGrammarInstance(filepath)
    return instance

def load_grammar_file(filepath):
    if _isRELFileName(filepath):
        return _loadRELGrammarFromFile(filepath)
    if _isGDLFileName(filepath):
        return _loadGDLGrammarFromFile(filepath)
    from .DirStorage import load_python_file 
    return load_python_file(filepath)
    
def _loadGDLGrammarFromFile(filepath):
    (_, _, fileBaseName, _) = getFileTuple(filepath)
    from ColonyDSL.Memory.Storage.Directory.BNF import bnf_file_to_productionset
    productionruleset, macrodic = bnf_file_to_productionset(filepath)
    parser = "descent"
    if "parser" in macrodic:
        parser = macrodic["parser"]
    instance = SymbolGrammar(fileBaseName, productionruleset, parser)
    return instance

class GrammarDirStorage(DirStorage):
    """generate instances of grammars"""
    def __init__(self, path):
        DirStorage.__init__(self, path, [".py", ".bnf", ".re"])

    def load(self, identifier:str, strictgrammar = True):
        from ColonyDSL.Exceptions import StorageException
        #TODO: What happens when we have > 1 result
        resultdic = self._searcher.search(identifier)
        for value in resultdic: 
            filename = value["filepath"]
            return load_grammar_file(filename)
        from ColonyDSL.Config import GLOBALCONFIG
        if strictgrammar != True and not GLOBALCONFIG.strictgrammar:
            from ColonyDSL.Type.Type import DummyType
            LOG.warning("Unable to load:" + identifier)
            return DummyType()
        raise StorageException("G", identifier)

    def summary_from_filename(self, filename):
        (_, _, fileBaseName, ext) = getFileTuple(filename)
        result = None
        if _isRELFileName(filename + ext):
            from ColonyDSL.Type.Grammar.Regular import RegularExpressionGrammar
            result =  {"iclass":"REG","identifier":fileBaseName, "filepath":filename, "ancestors":RegularExpressionGrammar.ancestors()}
        elif _isGDLFileName(filename + ext):
            result = {"iclass":"BNF","identifier":fileBaseName, "filepath":filename, "ancestors":SymbolGrammar.ancestors()}
        else:
            from ColonyDSL.Type.Grammar.Python import PythonGrammar
            result = {"iclass":"PythonGrammar","identifier":fileBaseName, "filepath":filename, "ancestors":PythonGrammar.ancestors()}
        from ColonyDSL.Abstract import InmutableDict
        return InmutableDict(result)

    def provided_iclasses(self) -> list:
        return ["PythonGrammar","REG","BNF"]

