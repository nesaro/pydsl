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

"""Global (per execution) elements"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"

from ColonyDSL.Abstract import Singleton
import logging
LOG = logging.getLogger("GlobalConfig")

def generate_memory_list() -> list:
    """loads default memories"""
    "", "/usr/share/ColonyDSL/"
    result = []
    from ColonyDSL.Memory.External.DirLibrary.Type import GrammarFileLibrary
    from ColonyDSL.Memory.External.DirLibrary.Function import BoardFileLibrary, TransformerDirLibrary, ProcedureFileLibrary
    from ColonyDSL.Memory.External.DictLibrary import FileTypeDictLibrary, ConceptDictLibrary, ConceptRelationDictLibrary
    from ColonyDSL.Memory.External.ListLibrary import ConceptRelationshipListLibrary
    from ColonyDSL.Memory.External.DirLibrary.Concept import ConceptFileLibrary
    from ColonyDSL.Memory.External.DirLibrary.Scheme import SchemeFileLibrary
    result.append(GrammarFileLibrary("/usr/share/ColonyDSL/lib_contrib/grammar/"))
    result.append(BoardFileLibrary("/usr/share/ColonyDSL/lib_contrib/board/"))
    result.append(TransformerDirLibrary("/usr/share/ColonyDSL/lib_contrib/transformer/"))
    result.append(ProcedureFileLibrary("/usr/share/ColonyDSL/lib_contrib/procedure/"))
    result.append(FileTypeDictLibrary("/usr/share/ColonyDSL/lib_contrib/dict/filetype.dict"))
    result.append(SchemeFileLibrary("/usr/share/ColonyDSL/lib_contrib/scheme/"))
    try:
        result.append(GrammarFileLibrary("./lib_contrib/grammar/"))
        result.append(SchemeFileLibrary("./lib_contrib/scheme/"))
        result.append(FileTypeDictLibrary("./lib_contrib/dict/filetype.dict"))
        result.append(ProcedureFileLibrary("./lib_contrib/procedure/"))
        result.append(TransformerDirLibrary("./lib_contrib/transformer/"))
        result.append(BoardFileLibrary("./lib_contrib/board/"))
    except IOError:
        pass
    return result


class GlobalConfig(metaclass = Singleton):
    """Execution time global configuration"""
    def __init__(self, strictgrammar = False, persistent_dir:str = None, debuglevel = 40):
        self.strictgrammar = strictgrammar #Allows to replace an unknown grammar to DummyGrammar
        self.persistent_dir = persistent_dir
        self.__memorylist = None #All known memories, sorted by preference  #Loaded when required
        self.__debuglevel = debuglevel
        self.lang = "es"
        if self.persistent_dir is None:
            try:
                import os
                if not os.path.exists(os.environ['HOME'] + "/.colony/"):
                    os.mkdir(os.environ['HOME'] + "/.colony/")                         
                self.persistent_dir = os.environ['HOME'] + "/.colony/persistent/"
                if not os.path.exists(self.persistent_dir):
                    os.mkdir(self.persistent_dir)                         
            except (OSError, KeyError):
                LOG.exception("Unable to create persistent dir")
       
    def load(self, filename):
        """Load config from file"""
        raise NotImplementedError
     
    def save(self):
        """Save config to file"""
        raise NotImplementedError
        
    @property
    def memorylist(self):
        if self.__memorylist == None:
            self.__memorylist = generate_memory_list()
        return self.__memorylist

    @property
    def debuglevel(self):
        return self.__debuglevel
    
    @debuglevel.setter
    def debuglevel(self, level:int):
        self.__debuglevel = level
    
VERSION = "ColonyDSL pre-version\n Copyright (C) 2008-2012 Néstor Arocha Rodríguez"
GLOBALCONFIG = GlobalConfig() #The only instance available
ERRORLIST = ["Grammar", "Timeout", "Transformer"]

def all_classes(module) -> set:
    """Returns all classes (introspection)"""
    import inspect
    result = set()
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            result.add(obj)
        elif inspect.ismodule(obj):
            if obj.__name__[:6] == "Colony":
                result = result.union(all_classes(obj))
    return result

def all_indexable_classes(module) -> set:
    """Returns all indexable classes (introspection)"""
    import inspect
    result = set()
    for name, obj in inspect.getmembers(module):
        from ColonyDSL.Abstract import Indexable
        if inspect.isclass(obj) and issubclass(obj, Indexable):
            result.add(obj)
        elif inspect.ismodule(obj):
            if obj.__name__[:6] == "Colony":
                result = result.union(all_indexable_classes(obj))
    return result

if __name__ == "__main__":
    import ColonyDSL
    print([x.__name__ for x in all_classes(ColonyDSL)])
    print([x.__name__ for x in all_indexable_classes(ColonyDSL)])
    from ColonyDSL.Memory.External.DirLibrary.Function import BoardFileLibrary
    a = BoardFileLibrary("/usr/share/ColonyDSL/lib_contrib/board/")
    a = a.load("simple-adder")
    print(a.ancestors())


