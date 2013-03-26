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

from .Memory import Memory
from pydsl.Memory.File.Python import getFileTuple
from pydsl.Abstract import InmutableDict
from pydsl.Memory.File.Regexp import load_re_from_file, summary_re_from_file
from pydsl.Memory.File.BNF import load_bnf_file, summary_bnf_file
from pydsl.Memory.File.Python import summary_python_file
import logging
LOG = logging.getLogger(__name__)

def _isGDLFileName(path):
    return path.endswith(".bnf")

def _isRELFileName(path):
    return path.endswith(".re")

#def re_file_to_summary(path)
#    (_, _, fileBaseName, _) = getFileTuple(filepath)
#    return {"iclass":"re","identifier":fileBaseName, "filepath":filepath}
#
#iclasseslist = [
#    {"iclass","extension":["py"],  "summary_from_file":, "load_from_file": },
#    {"extension":["re"], "summary_from_file": re_file_to_summary,"load_from_file":load_re_from_file},
#    {"extension":["bnf"], },
#]

class DirStorage(Memory):
    """A collection of elements stored inside a directory"""

    def __init__(self, dirpath, allowedextensions=(".py", ".bnf", ".re")):
        Memory.__init__(self)
        self.path = dirpath
        self._allowedextensions = allowedextensions
        from pydsl.Memory.Search.Searcher import MemorySearcher

        self._searcher = MemorySearcher(self)

    def __iter__(self):
        self.index = 0
        self.cache = []
        for filename in self.all_files():
            try:
                self.cache.append(self.summary_from_filename(filename))
            except (AttributeError,ImportError, TypeError) as e:
                LOG.debug("Error while loading %s file summary" % filename )
        return self

    def next(self):
        try:
            result = self.cache[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result
        

    @staticmethod
    def summary_from_filename(filepath):
        if _isRELFileName(filepath):
            result =  summary_re_from_file(filepath)
        elif _isGDLFileName(filepath):
            result = summary_bnf_file(filepath)
        else:
            result = summary_python_file(filepath)
        return InmutableDict(result)

    def all_files(self):
        import glob
        extensions = self._allowedextensions or [""]
        for extension in extensions:
            searchstring = self.path + "*" + extension
            tmpresult = glob.glob(searchstring)
            for result in tmpresult:
                if result.endswith("__init__.py"):
                    continue
                yield result


    def all_names(self):
        """Generates all Static Ids"""
        for fullname in self.all_files():
            (_, _, fileBaseName, fileExtension) = getFileTuple(fullname)
            if self._allowedextensions and fileExtension not in self._allowedextensions:
                continue
            yield fileBaseName.split(".")[0]

    def load(self, name, **kwargs):
        resultlist = self._searcher.search(name)
        if len(resultlist) > 1:
            LOG.error("Found two or more matches, FIXME: processing the first, should raise exception")
        if not resultlist:
            raise KeyError(self.__class__.__name__ + name)
        filepath = list(resultlist)[0]["filepath"]
        if _isRELFileName(filepath):
            return load_re_from_file(filepath)
        if _isGDLFileName(filepath):
            return load_bnf_file(filepath)
        from pydsl.Memory.File.Python import load_python_file
        return load_python_file(filepath, **kwargs)

    def __contains__(self, key):
        return key in self.all_names()

    def provided_iclasses(self):
        return set([x['iclass'] for x in self])

