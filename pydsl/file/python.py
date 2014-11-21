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

import imp

def getFileTuple(fullname):
    import os.path
    (dirName, fileName) = os.path.split(fullname)
    (fileBaseName, fileExtension) = os.path.splitext(fileName)
    return dirName, fileName, fileBaseName, fileExtension

def load_module(filepath, identifier = None):
    if identifier is None:
        (_, _, identifier, _) = getFileTuple(filepath)
    return imp.load_source(identifier, filepath)

def load_python_file(moduleobject):
    """ Try to create an indexable instance from a module"""
    if isinstance(moduleobject, str):
        moduleobject = load_module(moduleobject)
    if not hasattr(moduleobject, "iclass"):
        raise KeyError("Element" + str(moduleobject))
    iclass = getattr(moduleobject, "iclass")
    mylist = getattr(moduleobject, "__all__", None) or list(filter(lambda x:x[:1] != "_", (dir(moduleobject))))
    mylist.remove('iclass')
    resultdic = {}
    for x in mylist:
        resultdic[x] = getattr(moduleobject, x)
    if iclass == "SymbolGrammar":
        from pydsl.grammar.BNF import BNFGrammar
        return BNFGrammar(**resultdic)
    elif iclass == "PLY":
        from pydsl.grammar.definition import PLYGrammar
        return PLYGrammar(moduleobject)
    elif iclass == "MongoDict":
        from pydsl.grammar.definition import MongoGrammar
        return MongoGrammar(resultdic)
    elif iclass in ["PythonGrammar"]:
        from pydsl.grammar.definition import PythonGrammar
        return PythonGrammar(resultdic)
    elif iclass == "PythonTranslator":
        return resultdic
    elif iclass == "parsley":
        from pydsl.grammar.parsley import ParsleyGrammar
        return ParsleyGrammar(**resultdic)
    elif iclass == "pyparsing":
        return resultdic['root_symbol']
    else:
        raise ValueError(str(moduleobject))


