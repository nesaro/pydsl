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


__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"


import logging
LOG = logging.getLogger("Storage.Dict")
from .Memory import Memory

class DictStorage(Memory):
    """Stores element in a python file using a python dictionaty"""
    def __init__(self, fullpath):
        Memory.__init__(self)
        self._content = {}
        from pydsl.Memory.Search.Searcher import MemorySearcher
        self._searcher = MemorySearcher(self)
        from pydsl.Memory.File.Python import getFileTuple
        (_, _, fileBaseName, _) = getFileTuple(fullpath)
        import imp
        myobj = imp.load_source(fileBaseName, fullpath)
        self._content.update(myobj.mydict)

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

    def generate_all_summaries(self):
        """A list of all elements of full elements"""
        raise NotImplementedError
        
    def __contains__(self, index):
        return index in self._content

class RegexpDictStorage(DictStorage):
    def generate_all_summaries(self):# -> list:
        result = []
        from pydsl.Abstract import InmutableDict
        for key in self._content:
            result.append(InmutableDict({"identifier":key, "regexp":self._content[key]["regexp"], "iclass":"RegularExpressionGrammarTools"}))
        return result

    def load(self, index, **kwargs):
        import re
        if "flags" in self._content[index]:
            flags = 0
            if "i" in self._content[index]["flags"]:
                flags |= re.I
            return re.compile(self._content[index]["regexp"], flags)
        return re.compile(self._content[index]["regexp"])

    def provided_iclasses(self):# -> list:
        return ["re"]


class StrDictStorage(DictStorage):
    def generate_all_summaries(self):# -> list:
        result = []
        from pydsl.Abstract import InmutableDict
        for key in self._content:
            result.append(InmutableDict({"identifier":key, "content":self._content[key], "iclass":"str" }))
        return result

    def load(self, index):
        return self._content[index]

    def provided_iclasses(self):# -> list:
        return ["str"]

