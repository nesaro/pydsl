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
from pydsl.Abstract import InmutableDict

def load_module(filepath, identifier = None):
    if identifier is None:
        (_, _, identifier, _) = getFileTuple(filepath)
    import imp
    return imp.load_source(identifier, filepath)

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
        from pydsl.Function.ExternalProgram import ExternalProgramFileFunction
        return ExternalProgramFileFunction(**resultdic)
    elif iclass == "SymbolGrammar":
        from pydsl.Grammar.BNF import BNFGrammar
        return BNFGrammar(**resultdic)
    elif iclass == "PLY":
        from pydsl.Grammar.Definition import PLYGrammar
        return PLYGrammar(moduleobject)
    elif iclass == "MongoDict":
        from pydsl.Grammar.Definition import MongoGrammar
        return MongoGrammar(resultdic)
    elif iclass in ["PythonGrammar"]:
        return resultdic
    else:
        raise ValueError(str(moduleobject))


def getFileTuple(fullname):
    import os.path
    (dirName, fileName) = os.path.split(fullname)
    (fileBaseName, fileExtension) = os.path.splitext(fileName)
    return (dirName, fileName, fileBaseName, fileExtension) 

def summary_python_file(modulepath):
    import imp
    (_, _, fileBaseName, ext) = getFileTuple(modulepath)
    moduleobject = imp.load_source(fileBaseName, modulepath)
    result = {"identifier":fileBaseName, "iclass":moduleobject.iclass, "filepath":modulepath}
    if hasattr(moduleobject, "title"):
        result["title"] =  InmutableDict(moduleobject.title)
    if hasattr(moduleobject, "description"):
        result["description"] =  InmutableDict(moduleobject.description)
    if hasattr(moduleobject, "inputdic"):
        result["input"] = InmutableDict(moduleobject.inputdic)
        result["inputlist"] = tuple(moduleobject.inputdic.values())
    if hasattr(moduleobject, "outputdic"):
        result["output"] = InmutableDict(moduleobject.outputdic)
        result["outputlist"] = tuple(moduleobject.outputdic.values())
    if hasattr(moduleobject, "inputformat"):
        result["input"] = moduleobject.inputformat
    if hasattr(moduleobject, "outputformat"):
        result["output"] = moduleobject.outputformat
    return InmutableDict(result)

