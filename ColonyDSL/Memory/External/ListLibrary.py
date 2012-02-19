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

"""ListLibrary"""


__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


from abc import abstractmethod, ABCMeta

import logging
LOG = logging.getLogger("ListLibrary")
from .Library import Library

class ListLibrary(Library, metaclass = ABCMeta):
    """Stores element in a python file using a python list"""
    def __init__(self, fullpath:str):
        Library.__init__(self)
        self._content = {}
        from ColonyDSL.Memory.Search.Searcher import MemorySearcher
        self._searcher = MemorySearcher(self)
        from ColonyDSL.Config import GLOBALCONFIG
        from ColonyDSL.Memory.External.DirLibrary.DirLibrary import getFileTuple
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

    def __next__(self):
        try:
            result = self.cache[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    @abstractmethod
    def _generatekey(self, element):
        """Generates a identifier for the input element to use in this memory"""
        pass

    @abstractmethod
    def generate_all_summaries(self):
        """generates the full list of element summaries"""
        pass
        
    def __contains__(self, index):
        return index in self._content

class ConceptListLibrary(ListLibrary):
    def generate_all_summaries(self) -> list:
        result = []
        from ColonyDSL.Abstract import InmutableDict
        for key in self._content:
            result.append(InmutableDict({"identifier":key, "iclass":"Concept" }))
        return result

    def load(self, index):
        if index in self._content:
            from ColonyDSL.Concept.Concept import Concept
            return Concept(index)
        else:
            raise KeyError

    def _generatekey(self, element):
        return element

    def provided_iclasses(self):
        return ["Concept"]

class RelationListLibrary(ListLibrary):
    def generate_all_summaries(self) -> list:
        result = []
        from ColonyDSL.Abstract import InmutableDict
        for key in self._content:
            result.append(InmutableDict({"identifier":key, "rel":self._content[key]["rel"], "roledict":InmutableDict(self._content[key]["roledict"]), "iclass":"Relation" }))
        return result

    def load(self, index):
        from ColonyDSL.Concept.Relation import Relation
        return Relation(self._content[index]["rel"], self._content[index]["roledict"])

    def _generatekey(self, element):
        from ColonyDSL.Concept.Relation import Relation
        return Relation.generate_identifier(element["rel"], element["roledict"])

    def provided_iclasses(self):
        return ["Relation"]

class RelListLibrary(ListLibrary):
    def generate_all_summaries(self) -> list:
        result = []
        from ColonyDSL.Abstract import InmutableDict
        for key in self._content:
            result.append(InmutableDict({"identifier":key, "content":tuple(self._content[key]["content"]), "iclass":"Rel" }))
        return result

    def load(self, index):
        from ColonyDSL.Concept.Relation import Rel
        return Rel(self._content[index]["identifier"], self._content[index]["content"])

    def _generatekey(self, element):
        return element["identifier"]

    def provided_iclasses(self):
        return ["Rel"]
