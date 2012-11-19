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


__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pydsl.Abstract import Indexable

class Memory:
    """Memory Abstraction"""
    def __init__(self):
        pass

    def load(self, index, **kwargs):
        raise NotImplementedError
    
    def save(self, element):
        raise NotImplementedError

    def __iter__(self):
        """Must use summary abstraction"""
        raise NotImplementedError
    
    def next(self):
        raise NotImplementedError

    def __next__(self):
        return self.next()

    def __getitem__(self, index):
        return self.load(index)

    def __setitem__(self, index, value):
        return self.save(value, index)

    def indexer(self):
        from pydsl.Memory.Search.Indexer import Indexer
        return Indexer(self)
    
    def searcher(self):
        from pydsl.Memory.Search.Searcher import MemorySearcher
        return MemorySearcher(self.indexer())
    
    def search(self, query):
        return self.searcher().search(query)


class LocalMemory(Memory):
    """Execution time memory"""
    def __init__(self):
        self.content = {}
    
    def load(self, index):
        return self.content[index]
    
    def save(self, element, identifier):
        self.content[str(identifier)] = element
    
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
