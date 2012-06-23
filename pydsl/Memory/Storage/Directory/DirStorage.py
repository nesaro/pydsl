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


""" File Library class """

from abc import ABCMeta, abstractmethod
from ..Storage import Storage
import logging
LOG = logging.getLogger(__name__)

def load_attr_from_module(filepath, attributename):
    (_, _, fileBaseName, _) = getFileTuple(filepath)
    import imp
    try:
        grammarobject = imp.load_source(fileBaseName, filepath)
        return getattr(grammarobject, attributename)
    except (NameError, AttributeError):
        raise ImportError
    raise ImportError

def load_module(filepath):
    (_, _, fileBaseName, _) = getFileTuple(filepath)
    import imp
    return imp.load_source(fileBaseName, filepath), fileBaseName

def checkattr(moduleobject, attrlist:list) -> bool:
    for element in attrlist:
        if not hasattr(moduleobject, element):
            return False
    return True

def load_python_file(moduleobject, **kwargs):
    """ Try to create an indexable instance from a module"""
    if isinstance(moduleobject, str):
        moduleobject, identifier = load_module(moduleobject)
    if not hasattr(moduleobject, "iclass"):
        raise KeyError("Element" + identifier)
    iclass = getattr(moduleobject, "iclass")
    resultdic = kwargs
    mylist = list(filter(lambda x:x[:1] != "_" and x != "iclass", (dir(moduleobject))))
    for x in mylist:
        resultdic[x] = getattr(moduleobject, x)
    if iclass == "PythonTransformer":
        from pydsl.Function.Transformer.Python import PythonTransformer
        return PythonTransformer(**resultdic)
    elif iclass == "HostPythonTransformer":
        from pydsl.Function.Transformer.Python import HostPythonTransformer
        return HostPythonTransformer(**resultdic)
    elif iclass == "ExternalProgramTransformer":
        from pydsl.Function.Transformer.ExternalProgram import ExternalProgramTransformer
        return ExternalProgramTransformer(**resultdic)
    elif iclass == "PythonProcedure":
        from pydsl.Function.Procedure import PythonProcedure
        #instance = PythonProcedure(identifier, outputdic, server, moduleobject.function, title, description)
        return PythonProcedure(**resultdic)
    elif iclass == "ExternalProgramFileFunction":
        from pydsl.Function.File import ExternalProgramFileFunction
        return ExternalProgramFileFunction(**resultdic)
    elif iclass == "SimpleGrammarSetTransformer":
        from pydsl.Function.GrammarSetTransformer import SimpleGrammarSetTransformer
        return SimpleGrammarSetTransformer(**resultdic)
    elif iclass == "PythonGrammar":
        from pydsl.Grammar.Tool.Python import PythonGrammarTools
        return PythonGrammarTools(**resultdic)
    elif iclass == "HostPythonGrammar":
        from pydsl.Grammar.Tool.Python import HostPythonGrammarTools
        return HostPythonGrammarTools(**resultdic)
    elif iclass == "SymbolGrammar":
        from pydsl.Grammar.Tool.Symbol import SymbolGrammarTools
        return SymbolGrammarTools(**resultdic)
    elif iclass == "ExternalProgramType":
        from pydsl.Grammar.ExternalProgram import ExternalProgramChecker
        return ExternalProgramChecker(**resultdic)
    elif iclass == "FileType":
        from pydsl.Grammar.FileType import FileType
        return FileType(**resultdic)
    elif iclass == "Actor":
        from pydsl.Exchange.Actor import Actor
        return Actor(**resultdic)
    elif iclass == "Concept":
        from pydsl.Concept.Concept import Concept
        return Concept(**resultdic)
    else:
        raise ValueError

class DirStorage(Storage, metaclass = ABCMeta):
    """A collection of elements stored inside a directory"""
    def __init__(self, dirpath:str, allowedextensions:list = []):
        self.identifier = dirpath
        from pydsl.Config import GLOBALCONFIG
        resultdirpath = []
        self._allowedextensions = allowedextensions
        from pydsl.Memory.Search.Searcher import MemorySearcher
        self._searcher = MemorySearcher(self)

    def __iter__(self):
        self.index = 0
        self.cache = []
        for filename in self.all_files():
            self.cache.append(self.summary_from_filename(filename))
        return self

    def __next__(self):
        try:
            result = self.cache[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result
        

    def summary_from_filename(self, modulepath):
        (_, _, fileBaseName, _) = getFileTuple(modulepath)
        import imp
        moduleobject = imp.load_source(fileBaseName, modulepath)
        from pydsl.Abstract import InmutableDict
        result = {"identifier":fileBaseName, "iclass":moduleobject.iclass, "path":modulepath}
        if hasattr(moduleobject, "title"):
            from pydsl.Abstract import InmutableDict
            result["title"] =  InmutableDict(moduleobject.title)
        if hasattr(moduleobject, "description"):
            from pydsl.Abstract import InmutableDict
            result["description"] =  InmutableDict(moduleobject.description)
        return result

    def _search_files(self, string: str, exact:bool = True):
        """Search through library"""
        for filename in self.all_files():
            if exact:
                (_, _, fileBaseName, _) = getFileTuple(filename)
                if fileBaseName.strip() == string.strip():
                    yield filename
            else:
                if string.lower() in filename.lower():
                    yield filename

    def all_files(self):
        import glob
        if self._allowedextensions:
            for extension in self._allowedextensions:
                tmpresult = []
                searchstring = self.identifier + "*" + extension 
                tmpresult = glob.glob(searchstring)
                for result in tmpresult:
                    if result.endswith("__init__.py"):
                        continue
                    yield result 
        else:
            searchstring = self.identifier + "*" 
            for result in glob.glob(searchstring):
                yield result 


    def all_names(self):
        """Generates all Static Ids"""
        for fullname in self.all_files():
            (_, _, fileBaseName, fileExtension) = getFileTuple(fullname)
            if self._allowedextensions and fileExtension not in self._allowedextensions:
                continue
            yield fileBaseName.split(".")[0]

    def _load_module_from_library(self, identifier):
        """ Carga un modulo desde la libreria"""
        try:
            import imp
            moduleobject = imp.load_source(identifier, self.identifier + "/" + identifier + ".py")
        except (ImportError, IOError):
            pass
        else:
            return moduleobject
        raise ImportError

    def load(self, name, **kwargs):
        resultlist = self._searcher.search(name)
        if(len(resultlist) > 1):
            LOG.error("Found two or more matches, FIXME: processing the first, should raise exception")
        if len(resultlist) == 0:
            raise KeyError(self.__class__.__name__ + name)
        return load_python_file(list(resultlist)[0]["filepath"], **kwargs)

    def __contains__(self, key):
        return key in self.all_names()

def getFileTuple(fullname):
    import os.path
    (dirName, fileName) = os.path.split(fullname)
    (fileBaseName, fileExtension) = os.path.splitext(fileName)
    return (dirName, fileName, fileBaseName, fileExtension) 

class StrDirStorage(DirStorage):
    """Dir library for txt files"""
    def __init__(self, dirpath:str):
        DirStorage.__init__(self, dirpath)

    def summary_from_filename(self, filename) -> dict:
        #TODO Load first characters to summary
        _, filename, _, _ = getFileTuple(filename)
        return {"iclass":"str", "identifier":filename}

    def provided_iclasses(self) -> list:
        return ["str"]

