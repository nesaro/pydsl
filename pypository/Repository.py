#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of pypository.
#
#pypository is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pypository is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pypository.  If not, see <http://www.gnu.org/licenses/>.


__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)

class Repository(object):
    def load(self, index, **kwargs):
        raise NotImplementedError
    
    def save(self, element, identifier):
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

    @property
    def indexer(self):
        from pypository.search.Indexer import Indexer
        return Indexer(self)
    
    @property
    def searcher(self):
        from pypository.search.Searcher import MemorySearcher
        return MemorySearcher(self.indexer)
    
    def search(self, query):
        return self.searcher.search(query)

    def provided_iclasses(self):
        raise NotImplementedError
