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

"""Functions Library"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"

from .DirStorage import DirStorage
from ..File.Python import getFileTuple
from pydsl.Abstract import InmutableDict
import logging
LOG = logging.getLogger("Storage.Directory.Function")

class TransformerDirStorage(DirStorage):
    """generate instances of Grammar Transformers"""
    def __init__(self, path):
        DirStorage.__init__(self, path, [".py"])

    def provided_iclasses(self) -> list:
        return ["PythonTransformer", "HostPythonTransformer"]

    def load(self, identifier):
        """guess class, guess filename from id, and then call loadTInstance"""
        import imp
        for value in self._searcher.search(identifier): 
            try:
                imp.load_source(identifier, value["filepath"])
            except (ImportError, IOError):
                LOG.exception("Exception while loading: " + identifier)
            else:
                from pydsl.Memory.Storage.File.Board import load_python_f
                return load_python_f(value["filepath"])

        raise KeyError("Transformer: " + identifier)
    
    def summary_from_filename(self, modulepath):
        from pydsl.Function.Transformer.Python import PythonTransformer
        (_, _, fileBaseName, _) = getFileTuple(modulepath)
        import imp
        moduleobject = imp.load_source(fileBaseName, modulepath)
        try:
            result = {"identifier":fileBaseName,"iclass":moduleobject.iclass, "filepath":modulepath}
            if hasattr(moduleobject, "title"):
                result["title"] =  InmutableDict(moduleobject.title)
            if hasattr(moduleobject, "description"):
                result["description"] =  InmutableDict(moduleobject.description)
            if hasattr(moduleobject, "inputdic"):
                result["input"] = InmutableDict(moduleobject.inputdic)
            if hasattr(moduleobject, "outputdic"):
                result["output"] = InmutableDict(moduleobject.outputdic)
            if hasattr(moduleobject, "inputformat"):
                result["input"] = moduleobject.inputformat
            if hasattr(moduleobject, "outputformat"):
                result["output"] = moduleobject.outputformat

            return InmutableDict(result)
        except AttributeError:
            #LOG.exception(modulepath)
            return InmutableDict()
        except ValueError:
            LOG.exception("Error: non-indexable element while loading " + modulepath)
            return InmutableDict()

class BoardDirStorage(DirStorage):
    """Loads boards from library"""
    def __init__(self, path):
        DirStorage.__init__(self, path, [".board"])

    def load(self, identifier):
        searchresult = self._searcher.search(identifier)
        for result in searchresult:
            #TODO assert(len(self._search(identifier) == 2)) 
            from pydsl.Memory.Storage.File.Board import load_board_file
            return load_board_file(result["filepath"])
        raise KeyError("Board" + identifier)

    def provided_iclasses(self) -> list:
        return ["Board"]



