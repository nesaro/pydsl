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

"""Grammar FileLibraries"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


import logging
LOG = logging.getLogger("Storage.Directory.Grammar")
from .DirStorage import DirStorage, getFileTuple

def _isGDLFileName(path):
    return path.endswith(".bnf")

def _isRELFileName(path):
    return path.endswith(".re")

def load_grammar_file(filepath):
    if _isRELFileName(filepath):
        from pydsl.Memory.Storage.Directory.Regexp import load_re_from_file
        return load_re_from_file(filepath)
    if _isGDLFileName(filepath):
        return _loadGDLGrammarFromFile(filepath)
    from .DirStorage import load_python_file 
    return load_python_file(filepath)
    
def _loadGDLGrammarFromFile(filepath):
    (_, _, fileBaseName, _) = getFileTuple(filepath)
    from pydsl.Memory.Storage.Directory.BNF import bnf_file_to_productionset
    bnfgrammar = bnf_file_to_productionset(filepath)
    return bnfgrammar

class GrammarDirStorage(DirStorage):
    """generate instances of grammars"""
    def __init__(self, path):
        DirStorage.__init__(self, path, [".py", ".bnf", ".re"])

    def load(self, identifier:str, strictgrammar = True):
        #TODO: What happens when we have > 1 result
        resultdic = self._searcher.search(identifier)
        for value in resultdic: 
            filename = value["filepath"]
            return load_grammar_file(filename)
        from pydsl.Config import GLOBALCONFIG
        if strictgrammar != True and not GLOBALCONFIG.strictgrammar:
            from pydsl.Grammar.Checker import DummyChecker
            LOG.warning("Unable to load:" + identifier)
            return DummyChecker()
        raise KeyError("Grammar" + identifier)

    def summary_from_filename(self, filename):
        (_, _, fileBaseName, ext) = getFileTuple(filename)
        result = None
        if _isRELFileName(filename + ext):
            result =  {"iclass":"re","identifier":fileBaseName, "filepath":filename}
        elif _isGDLFileName(filename + ext):
            result = {"iclass":"BNFGrammar","identifier":fileBaseName, "filepath":filename}
        else:
            from pydsl.Grammar.Tool.Python import PythonGrammarTools
            result = {"iclass":"PythonGrammarTools","identifier":fileBaseName, "filepath":filename}
        from pydsl.Abstract import InmutableDict
        return InmutableDict(result)

    def provided_iclasses(self) -> list:
        return ["PythonGrammarTools","re","BNFGrammar"]

