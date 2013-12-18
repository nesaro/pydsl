#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of pypository.
#
#pypository is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pypository is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pypository.  If not, see <http://www.gnu.org/licenses/>.

""" Directory storage """

from .Repository import Repository
from pypository.utils import ImmutableDict, getFileTuple
import logging
LOG = logging.getLogger(__name__)


class DirRepository(Repository):
    """A collection of elements stored inside a directory"""
    def __init__(self, dirpath, formatlist):
        Repository.__init__(self)
        self.formatlist = formatlist
        self.path = dirpath
        from pypository.search.Searcher import Searcher
        self._searcher = Searcher(self)

    def __iter__(self):
        self.index = 0
        self.cache = []
        for filename in self.all_files():
            try:
                self.cache.append(self.summary_from_filename(filename))
            except (AttributeError,ImportError, TypeError) as e:
                LOG.debug("Error while loading %s file summary %s" % (filename, e) )
        return self

    def summary_from_filename(self, filepath):
        entry = [x for x in self.formatlist if filepath.endswith(x["extension"])][0]
        return ImmutableDict(entry["summary_from_file"](filepath))

    @property
    def allowed_extensions(self):
        return [x["extension"] for x in self.formatlist]

    def next(self):
        try:
            result = self.cache[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result
        
    def all_files(self):
        import glob
        extensions = self.allowed_extensions or [""]
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
            if self.allowed_extensions and fileExtension not in self.allowed_extensions:
                continue
            yield fileBaseName.split(".")[0]

    def load(self, name):
        result = self._searcher.search(name)
        if len(result) > 1:
            LOG.error("Found two or more matches, FIXME: processing the first, should raise exception")
        if not result:
            raise KeyError(self.__class__.__name__ + name)
        filepath = list(result)[0]["filepath"]
        entries = [x for x in self.formatlist if filepath.endswith(x["extension"])]
        for entry in entries:
            try:
                return entry["load_from_file"](filepath)
            except ValueError:
                continue
        raise ValueError("Unable to open: %s" % name)


    def __contains__(self, key):
        return key in self.all_names()

    def provided_iclasses(self):
        return set([x['iclass'] for x in self])

