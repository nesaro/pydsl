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

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"

from ..File.Grammar import _isRELFileName, _isGDLFileName, load_grammar_file

import logging
LOG = logging.getLogger("Storage.Directory.Grammar")
from .DirStorage import DirStorage

class GrammarDirStorage(DirStorage):
    """generate instances of grammars"""
    def __init__(self, path):
        DirStorage.__init__(self, path, [".py", ".bnf", ".re"])

    def load(self, identifier:str):
        #TODO: What happens when we have > 1 result
        resultdic = self._searcher.search(identifier)
        for value in resultdic: 
            filename = value["filepath"]
            return load_grammar_file(filename)
        raise KeyError("Grammar " + identifier)

    def provided_iclasses(self) -> list:
        return ["PythonGrammarTools","re","BNFGrammar"]

