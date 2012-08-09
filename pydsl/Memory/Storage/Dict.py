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

"""Dictionary based library"""


__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


from abc import abstractmethod, ABCMeta

import logging
LOG = logging.getLogger("Storage.Dict")
from .Storage import Storage

class DictStorage(Storage, metaclass = ABCMeta):
    """Stores element in a python file using a python dictionaty"""
    def __init__(self, fullpath:str):
        Storage.__init__(self)
        self._content = {}
        from pydsl.Memory.Search.Searcher import MemorySearcher
        self._searcher = MemorySearcher(self)
        from pydsl.Config import GLOBALCONFIG
        from pydsl.Memory.Storage.File.Python import getFileTuple
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

class RegexpDictStorage(DictStorage):
    def generate_all_summaries(self) -> list:
        result = []
        from pydsl.Abstract import InmutableDict
        from pydsl.Grammar.FileType import FileType
        for key in self._content:
            result.append(InmutableDict({"identifier":key, "regexp":self._content[key]["regexp"], "iclass":"RegularExpressionGrammarTools" , "ancestors":FileType.ancestors()}))
        return result

    def load(self, index, **kwargs):
        import re
        if "flags" in self._content[index]:
            flags = 0
            if "i" in self._content[index]["flags"]:
                flags |= re.I
            return re.compile(self._content[index]["regexp"], flags)
        return re.compile(self._content[index]["regexp"])

    def provided_iclasses(self) -> list:
        return ["re"]


class FileTypeDictStorage(DictStorage):
    def generate_all_summaries(self) -> list:
        result = []
        from pydsl.Abstract import InmutableDict
        from pydsl.Grammar.FileType import FileType
        for key in self._content:
            result.append(InmutableDict({"identifier":key, "regexp":self._content[key], "iclass":"FileType" , "ancestors":FileType.ancestors()}))
        return result

    def load(self, index, **kwargs):
        from pydsl.Grammar.FileType import FileType
        return FileType(self._content[index])

    def provided_iclasses(self) -> list:
        return ["FileType"]


class StrDictStorage(DictStorage):
    def generate_all_summaries(self) -> list:
        result = []
        from pydsl.Abstract import InmutableDict
        for key in self._content:
            result.append(InmutableDict({"identifier":key, "content":self._content[key], "iclass":"str" }))
        return result

    def load(self, index):
        return self._content[index]

    def provided_iclasses(self) -> list:
        return ["str"]

