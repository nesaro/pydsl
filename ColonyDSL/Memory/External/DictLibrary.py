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

"""Dictionary based library"""


__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


from abc import abstractmethod, ABCMeta

import logging
LOG = logging.getLogger("DictLibrary")
from .Library import Library

class DictLibrary(Library, metaclass = ABCMeta):
    """Stores element in a python file using a python dictionaty"""
    def __init__(self, fullpath:str):
        Library.__init__(self)
        self._content = {}
        from ColonyDSL.Memory.Search.Searcher import MemorySearcher
        self._searcher = MemorySearcher(self)
        from ColonyDSL.GlobalConfig import GLOBALCONFIG
        from ColonyDSL.Memory.External.DirLibrary.DirLibrary import getFileTuple
        (_, _, fileBaseName, _) = getFileTuple(fullpath)
        import imp
        myobj = imp.load_source(fileBaseName, fullpath)
        self._content.update(myobj.mydict)

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
    def generate_all_summaries(self):
        """A list of all elements of full elements"""
        pass
        
    def __contains__(self, index):
        return index in self._content

class FileTypeDictLibrary(DictLibrary):
    def generate_all_summaries(self) -> list:
        result = []
        from ColonyDSL.Abstract import InmutableDict
        from ColonyDSL.Type.FileType import FileType
        for key in self._content:
            result.append(InmutableDict({"identifier":key, "regexp":self._content[key], "iclass":"FileType" , "ancestors":FileType.ancestors()}))
        return result

    def load(self, index):
        from ColonyDSL.Type.FileType import FileType
        return FileType(self._content[index])

    def provided_iclasses(self) -> list:
        return ["FileType"]

class ConceptDictLibrary(DictLibrary):
    def generate_all_summaries(self) -> list:
        result = []
        from ColonyDSL.Abstract import InmutableDict
        for key in self._content:
            result.append(InmutableDict({"identifier":key, "title":InmutableDict(self._content[key]["title"]),"description":InmutableDict(self._content[key]["description"]) ,"iclass":"Concept" }))
        return result

    def load(self, index):
        from ColonyDSL.Concept.Concept import Concept
        return Concept(index, self._content[index]["title"], self._content[index]["description"])

class ConceptRelationDictLibrary(DictLibrary):
    def generate_all_summaries(self) -> list:
        result = []
        from ColonyDSL.Abstract import InmutableDict
        for key in self._content:
            result.append(InmutableDict({"identifier":key, "title":InmutableDict(self._content[key]["title"]),"description":InmutableDict(self._content[key]["description"]) ,"rolelist":tuple(self._content[key]["rolelist"]), "iclass":"ConceptRelation" }))
        return result

    def load(self, index):
        from ColonyDSL.Concept.Relation import ConceptRelation
        return ConceptRelation(index, self._content[index]["rolelist"], self._content[index]["title"], self._content[index]["description"])

class StrDictLibrary(DictLibrary):
    def generate_all_summaries(self) -> list:
        result = []
        from ColonyDSL.Abstract import InmutableDict
        for key in self._content:
            result.append(InmutableDict({"identifier":key, "content":self._content[key], "iclass":"str" }))
        return result

    def load(self, index):
        return self._content[index]

    def provided_iclasses(self) -> list:
        return ["str"]

