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


""" Directory storage """

from ..Storage import Storage
from ..File.Python import getFileTuple
from ..File.Grammar import _isRELFileName, _isGDLFileName
from pydsl.Abstract import InmutableDict
import logging
LOG = logging.getLogger(__name__)

class DirStorage(Storage):
    """A collection of elements stored inside a directory"""
    def __init__(self, dirpath, allowedextensions = []):
        self.path = dirpath
        from pydsl.Config import GLOBALCONFIG
        resultdirpath = []
        self._allowedextensions = allowedextensions
        from pydsl.Memory.Search.Searcher import MemorySearcher
        self._searcher = MemorySearcher(self)

    def __iter__(self):
        self.index = 0
        self.cache = []
        for filename in self.all_files():
            try:
                self.cache.append(self.summary_from_filename(filename))
            except (AttributeError,ImportError) as e:
                LOG.debug("Error while loading %s file summary" % filename )
        return self

    def next(self):
        try:
            result = self.cache[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result
        

    def summary_from_filename(self, modulepath):
        (_, _, fileBaseName, ext) = getFileTuple(modulepath)
        result = None
        if _isRELFileName(modulepath):
            result =  {"iclass":"re","identifier":fileBaseName, "filepath":modulepath}
        elif _isGDLFileName(modulepath):
            result = {"iclass":"BNFGrammar","identifier":fileBaseName, "filepath":modulepath}
        elif (modulepath).endswith(".board"):
            result = {"iclass":"Board", "identifier":fileBaseName, "filepath":modulepath}
        else:
            import imp
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

    def _search_files(self, string, exact = True):
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
                searchstring = self.path + "*" + extension 
                tmpresult = glob.glob(searchstring)
                for result in tmpresult:
                    if result.endswith("__init__.py"):
                        continue
                    yield result 
        else:
            searchstring = self.path + "*" 
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
        try:
            import imp
            moduleobject = imp.load_source(identifier, self.path + "/" + identifier + ".py")
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

    def provided_iclasses(self):
        return set([x['iclass'] for x in self])

