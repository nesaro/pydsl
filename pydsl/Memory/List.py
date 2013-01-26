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

"""ListLibrary"""
from pydsl.Abstract import InmutableDict
import logging
LOG = logging.getLogger("Storage.List")
from pydsl.Memory.Memory import Memory
from pydsl.Alphabet.Definition import Encoding



__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"


class ListStorage(Memory):
    """Stores element in a python file using a python list"""
    def __init__(self, fullpath):
        Memory.__init__(self)
        self._content = {}
        from pydsl.Memory.Search.Searcher import MemorySearcher
        self._searcher = MemorySearcher(self)
        from pydsl.Memory.File.Python import getFileTuple
        (_, _, fileBaseName, _) = getFileTuple(fullpath)
        import imp
        myobj = imp.load_source(fileBaseName, fullpath)
        for element in myobj.mylist:
            self._content[self._generatekey(element)] = element

    def __iter__(self):
        self.index = 0
        self.cache = []
        self.cache += self.generate_all_summaries()
        return self

    def next(self):
        try:
            result = self.cache[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    def _generatekey(self, element):
        """Generates a identifier for the input element to use in this memory"""
        raise NotImplementedError

    def generate_all_summaries(self):
        """generates the full list of element summaries"""
        raise NotImplementedError
        
    def __contains__(self, index):
        return index in self._content


class EncodingStorage(ListStorage):
    def _generatekey(self, element):
        return element

    def load(self, index):
        return Encoding(index)

    def generate_all_summaries(self):
        result = []
        for x in self._content:
            result.append(InmutableDict({"identifier":x, "value":x, "iclass":"Encoding"}))
        return result
