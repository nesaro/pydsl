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


__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2011, Néstor Arocha Rodríguez"
__email__ = "nesaro@colonymbus.com"

import logging
LOG = logging.getLogger("Memory")
from abc import ABCMeta, abstractmethod
from ColonyDSL.Abstract import Indexable

class Memory(metaclass = ABCMeta):
    """Memory Abstraction"""
    @abstractmethod
    def load(self, index):
        pass
    
    @abstractmethod
    def save(self, element):
        pass

    @abstractmethod
    def __iter__(self):
        """Debe trabajar con summary"""
        pass
    
    @abstractmethod
    def __next__(self):
        """Debe trabajar con summary"""
        pass
    
    def __getitem__(self, index):
        return self.load(index)

    def indexer(self):
        from ColonyDSL.Memory.Search.Indexer import Indexer
        return Indexer(self)
    
    def searcher(self):
        from ColonyDSL.Memory.Search.Searcher import MemorySearcher
        return MemorySearcher(self.indexer())
    
class LocalMemory(Memory):
    """Executrion time memory"""
    def __init__(self):
        self.content = {}
    
    def load(self, index):
        from ColonyDSL.Identifier import Identifier
        if isinstance(index, Identifier):
            index = str(index)
        return self.content[index]
    
    def save(self, element:Indexable):
        self.content[str(element.identifier)] = element
    
    def __delitem__(self, key):
        del self.content[key]

    def __contains__(self, index):
        return index in self.content
    
    def __iter__(self):
        self.cacheindex = 0
        self.cache = []
        for element in self.content.values():
            self.cache.append(element.summary)
        return self
    
    def __next__(self):
        try:
            result = self.cache[self.cacheindex]
        except IndexError:
            raise StopIteration
        self.cacheindex += 1
        return result
