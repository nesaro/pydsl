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


"""
guess which types are the input data. 
It works like the unix file command
"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


import logging
LOG = logging.getLogger("Guess")

def guess(inputstring, memorylist = []) -> set:
    from ColonyDSL.Memory.Search.Searcher import MemorySearcher
    from ColonyDSL.Memory.External.DirLibrary.Type import GrammarFileLibrary 
    from ColonyDSL.Memory.External.DictLibrary import FileTypeDictLibrary
    if not memorylist:
        try:
            glib1 = GrammarFileLibrary("./lib_contrib/grammar/")
            ftdl1 = FileTypeDictLibrary("./lib_contrib/dict/filetype.dict")
        except IOError:
            pass
        else:
            memorylist.append(glib1)
            memorylist.append(ftdl1)
        memorylist.append(GrammarFileLibrary("/usr/share/ColonyDSL/lib_contrib/grammar/"))
        memorylist.append(FileTypeDictLibrary("/usr/share/ColonyDSL/lib_contrib/dict/filetype.dict"))
    searcher = MemorySearcher([x.indexer() for x in memorylist])
    result = set()
    for summary in searcher.search():
        typ = None
        name = None
        try:
            for mem in memorylist:
                if summary["identifier"] in mem:
                    name = summary["identifier"]
                    typ = mem.load(name)
                    break
            if typ.check(inputstring):
                result.add(str(name))
        except TypeError:
            continue
    return result

