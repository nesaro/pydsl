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

"""Wrapper Classes"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger("Wrapper")
from abc import ABCMeta, abstractmethod, abstractproperty
from ColonyDSL.Memory.Storage.Loader import load_function, load_type

class Cstr(str):
    """String wrapper"""
    def __init__(self, *args, **kwargs):
        str.__init__(*args, **kwargs)
        self.grammarlist = None
        self.functionlist = None
            
    def guess(self):
        if self.grammarlist == None:
            from ColonyDSL.Interaction.Guess import guess
            self.grammarlist = guess(self)
        return self.grammarlist

    def check(self, grammar):
        return grammar in self.guess()

    def available_transforms(self):
        if self.functionlist == None:
            from ColonyDSL.Memory.Search.Searcher import MemorySearcher
            from ColonyDSL.Memory.Search.Indexer import Indexer
            from ColonyDSL.Config import GLOBALCONFIG
            searcher = MemorySearcher([Indexer(x) for x in GLOBALCONFIG.memorylist])
            resultlist = []
            for element in self.guess():
                resultlist += searcher.search({"input":{"$part":{"input":element}}})
            self.functionlist = resultlist
        return self.functionlist



class FunctionsMeta(type):
    def __dir__(cls):
        from ColonyDSL.Memory.Search.Searcher import MemorySearcher
        from ColonyDSL.Memory.Search.Indexer import Indexer
        from ColonyDSL.Config import GLOBALCONFIG
        searcher = MemorySearcher([Indexer(x) for x in GLOBALCONFIG.memorylist])
        return [ x["identifier"] for x in searcher.search({"ancestors":{"$in":"Function"}})]

    def __getattr__(cls, key):
        return load_function(key)

class Functions(metaclass=FunctionsMeta):
    pass



