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

import logging
LOG = logging.getLogger(__name__)

def load_module(filepath):
    (_, _, fileBaseName, _) = getFileTuple(filepath)
    import imp
    return imp.load_source(fileBaseName, filepath)

def load_python_file(moduleobject, **kwargs):
    """ Try to create an indexable instance from a module"""
    if isinstance(moduleobject, str):
        moduleobject = load_module(moduleobject)
    if not hasattr(moduleobject, "iclass"):
        raise KeyError("Element" + str(moduleobject))
    iclass = getattr(moduleobject, "iclass")
    resultdic = kwargs
    mylist = list(filter(lambda x:x[:1] != "_" and x != "iclass", (dir(moduleobject))))
    for x in mylist:
        resultdic[x] = getattr(moduleobject, x)
    if iclass == "PythonTransformer":
        from pydsl.Function.Python import PythonTransformer
        return PythonTransformer(**resultdic)
    elif iclass == "HostPythonTransformer":
        from pydsl.Function.Python import HostPythonTransformer
        return HostPythonTransformer(**resultdic)
    elif iclass == "ExternalProgramTransformer":
        from pydsl.Function.ExternalProgram import ExternalProgramTransformer
        return ExternalProgramTransformer(**resultdic)
    elif iclass == "ExternalProgramFileFunction":
        from pydsl.Function.File import ExternalProgramFileFunction
        return ExternalProgramFileFunction(**resultdic)
    elif iclass == "PythonGrammar":
        return resultdic
    elif iclass == "SymbolGrammar":
        from pydsl.Grammar.Tool.Symbol import SymbolGrammarTools
        return SymbolGrammarTools(**resultdic)
    elif iclass == "ExternalProgramType":
        from pydsl.Grammar.ExternalProgram import ExternalProgramChecker
        return ExternalProgramChecker(**resultdic)
    elif iclass == "FileType":
        from pydsl.Grammar.FileType import FileType
        return FileType(**resultdic)
    elif iclass == "MongoDict":
        return resultdic
    else:
        raise ValueError


def getFileTuple(fullname):
    import os.path
    (dirName, fileName) = os.path.split(fullname)
    (fileBaseName, fileExtension) = os.path.splitext(fileName)
    return (dirName, fileName, fileBaseName, fileExtension) 

