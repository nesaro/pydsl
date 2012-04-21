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


""" File Library class """

from abc import ABCMeta, abstractmethod
from ..Storage import Storage
import logging
LOG = logging.getLogger("DirStorage")

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

def load_python_file(moduleobject, identifier = None, ecuid = None, server = None):
    """ Try to create an indexable instance from a module"""
    if isinstance(moduleobject, str):
        moduleobject, identifier = load_module(moduleobject)
    if not hasattr(moduleobject, "iclass"):
        from ColonyDSL.Exceptions import StorageException
        raise StorageException("Element", identifier)
    iclass = getattr(moduleobject, "iclass")
    resultdic = {}
    mylist = list(filter(lambda x:x[:1] != "_" and x != "iclass", (dir(moduleobject))))
    for x in mylist:
        resultdic[x] = getattr(moduleobject, x)
    if iclass == "PythonTransformer":
        resultdic["ecuid"] = ecuid
        resultdic["server"] = server
        from ColonyDSL.Function.Transformer.Python import PythonTransformer
        return PythonTransformer(**resultdic)
    elif iclass == "HostPythonTransformer":
        resultdic["ecuid"] = ecuid
        resultdic["server"] = server
        from ColonyDSL.Function.Transformer.Python import HostPythonTransformer
        return HostPythonTransformer(**resultdic)
    elif iclass == "ExternalProgramTransformer":
        resultdic["ecuid"] = ecuid
        resultdic["server"] = server
        from ColonyDSL.Function.Transformer.ExternalProgram import ExternalProgramTransformer
        return ExternalProgramTransformer(**resultdic)
    elif iclass == "PythonProcedure":
        from ColonyDSL.Function.Procedure import PythonProcedure
        #instance = PythonProcedure(identifier, outputdic, server, moduleobject.function, title, description)
        return PythonProcedure(**resultdic)
    elif iclass == "ExternalProgramFileFunction":
        from ColonyDSL.Function.File import ExternalProgramFileFunction
        return ExternalProgramFileFunction(**resultdic)
    elif iclass == "SimpleGrammarSetTransformer":
        resultdic["server"] = server
        from ColonyDSL.Function.GrammarSetTransformer import SimpleGrammarSetTransformer
        return SimpleGrammarSetTransformer(**resultdic)
    elif iclass == "PythonGrammar":
        from ColonyDSL.Type.Grammar.Python import PythonGrammar
        return PythonGrammar(**resultdic)
    elif iclass == "HostPythonGrammar":
        from ColonyDSL.Type.Grammar.Python import HostPythonGrammar
        return HostPythonGrammar(**resultdic)
    elif iclass == "SymbolGrammar":
        from ColonyDSL.Type.Grammar.Symbol import SymbolGrammar
        return SymbolGrammar(**resultdic)
    elif iclass == "ExternalProgramType":
        from ColonyDSL.Type.ExternalProgram import ExternalProgramType
        return ExternalProgramType(**resultdic)
    elif iclass == "FileType":
        from ColonyDSL.Type.FileType import FileType
        return FileType(**resultdic)
    elif iclass == "Scheme":
        from ColonyDSL.Abstraction.Scheme import Scheme
        return Scheme(**resultdic)
    elif iclass == "Concept":
        from ColonyDSL.Concept.Concept import Concept
        return Concept(**resultdic)
    else:
        raise ValueError

class DirStorage(Storage, metaclass = ABCMeta):
    """A collection of elements stored inside a directory"""
    def __init__(self, dirpath:str, allowedextensions:list = []):
        self.identifier = dirpath
        from ColonyDSL.Config import GLOBALCONFIG
        resultdirpath = []
        self._allowedextensions = allowedextensions
        from ColonyDSL.Memory.Search.Searcher import MemorySearcher
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
        
    @abstractmethod
    def summary_from_filename(self, filename) -> dict:
        pass

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

    def load(self, name):
        resultlist = self._searcher.search(name)
        if(len(resultlist) > 1):
            LOG.error("Found two or more matches, FIXME: processing the first, should raise exception")
        if len(resultlist) == 0:
            from ColonyDSL.Exceptions import StorageException
            raise StorageException(self.__class__.__name__, name)
        return load_python_file(list(resultlist)[0]["filepath"])

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

