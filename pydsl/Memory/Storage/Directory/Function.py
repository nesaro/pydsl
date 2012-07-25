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
import logging
LOG = logging.getLogger("Storage.Directory.Function")

class TransformerDirStorage(DirStorage):
    """generate instances of Grammar Transformers"""
    def __init__(self, path):
        DirStorage.__init__(self, path, [".py"])

    def provided_iclasses(self) -> list:
        return ["PythonTransformer", "HostPythonTransformer"]

    def load(self, identifier, server = None, ecuid=None):
        """guess class, guess filename from id, and then call loadTInstance"""
        import imp
        for value in self._searcher.search(identifier): 
            try:
                imp.load_source(identifier, value["filepath"])
            except (ImportError, IOError):
                LOG.exception("Exception while loading: " + identifier)
            else:
                return load_python_f(value["filepath"], server)

        raise KeyError("Transformer" + identifier)
    
    def summary_from_filename(self, modulepath):
        from pydsl.Function.Transformer.Python import PythonTransformer
        (_, _, fileBaseName, _) = getFileTuple(modulepath)
        import imp
        moduleobject = imp.load_source(fileBaseName, modulepath)
        from pydsl.Abstract import InmutableDict
        try:
            result = {"identifier":fileBaseName,"iclass":moduleobject.iclass, "filepath":modulepath, "ancestors":PythonTransformer.ancestors()}
            if hasattr(moduleobject, "title"):
                from pydsl.Abstract import InmutableDict
                result["title"] =  InmutableDict(moduleobject.title)
            if hasattr(moduleobject, "description"):
                from pydsl.Abstract import InmutableDict
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


    def load(self, identifier, server = None, ecuid = None):
        searchresult = self._searcher.search(identifier)
        if not searchresult:
            raise Exception
        for result in searchresult:
            #TODO assert(len(self._search(identifier) == 2)) 
            return load_board_file(result["filepath"], server = server, ecuid = ecuid)

        raise KeyError("Board" + identifier)

    def summary_from_filename(self, filename):
        from pydsl.Function.Transformer.Board import Board
        from pydsl.Abstract import InmutableDict
        (_, _, fileBaseName, _) = getFileTuple(filename)
        return InmutableDict({"iclass":"Board", "identifier":fileBaseName, "filepath":filename, "ancestors":Board.ancestors()})

    def provided_iclasses(self) -> list:
        return ["Board"]



class ProcedureDirStorage(DirStorage):
    """Procedure Library"""
    def __init__(self, path):
        DirStorage.__init__(self, path, [".py"])

    def summary_from_filename(self, filename):
        (_, _, fileBaseName, _) = getFileTuple(filename)
        return {"iclass":"Procedure","identifier":fileBaseName, "filepath":filename}

    def load(self, identifier, server = None):
        """guess class, guess filename from id, and then call loadTInstance"""
        import imp
        try:
            imp.load_source(identifier, self.identifier + "/" + identifier + ".py")
        except (ImportError, IOError):
            pass
        else:
            return load_python_f(identifier, server)

        raise KeyError("Procedure" + identifier)

    def provided_iclasses(self) -> list:
        return ["Procedure"]

    def all_files_generator(self):
        """Generates (inputlist, outputlist, name, description) from T list"""
        for elementname in self.allElementStaticIdGenerator():
            try:
                instance = self.load(elementname)
            except TypeError:
                continue
            except KeyError:
                continue
            except ImportError:
                continue
            except NameError:
                continue
            exfun = lambda x:getattr(x,"name").split(".")[0]
            yield (map(exfun, elementname, instance.description))
            #instance.outputchanneldic.values()),
        

