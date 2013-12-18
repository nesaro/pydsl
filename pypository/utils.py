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

"""Abstract Classes"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)

class ImmutableDict(dict):
    """A dict with a hash method for dictionary use"""
    def __hash__(self):
        if not self:
            return 0
        items = tuple(self.items())
        res = hash(items[0])
        for item in items[1:]:
            res ^= hash(item)
        return res

    def __eq__(self, other):
        if len(self.keys()) != len(other.keys()):
            return False
        for key in self:
            if other[key] != self.__getitem__(key):
                return False
        return True

    def __setitem__(self, key, value):
        raise Exception

def getFileTuple(fullname):
    import os.path
    (dirName, fileName) = os.path.split(fullname)
    (fileBaseName, fileExtension) = os.path.splitext(fileName)
    return dirName, fileName, fileBaseName, fileExtension

def load_module(filepath, identifier = None):
    import imp
    if identifier is None:
        (_, _, identifier, _) = getFileTuple(filepath)
    return imp.load_source(identifier, filepath)

