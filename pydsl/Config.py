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

"""Global (per execution) elements"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

from pydsl.Abstract import Singleton
import logging
LOG = logging.getLogger(__name__)
from pkg_resources import Requirement, resource_filename, DistributionNotFound


def generate_memory_list(): #-> list:
    """loads default memories"""
    result = []
    from pydsl.Memory.Storage.Directory import DirStorage
    from pydsl.Memory.Storage.Dict import RegexpDictStorage
    try:
        dirname = resource_filename("pydsl.contrib", "")
    except DistributionNotFound:
        pass
    else:
        result.append(DirStorage(dirname + "/grammar/"))
        result.append(DirStorage(dirname + "/board/"))
        result.append(DirStorage(dirname + "/transformer/"))
        result.append(RegexpDictStorage(dirname + "/dict/regexp.dict"))
    return result


class GlobalConfig(object):
    """Execution time global configuration"""
    def __init__(self, persistent_dir=None, debuglevel=40):
        self.persistent_dir = persistent_dir
        self.__memorylist = None  # default memories, sorted by preference
        self.__debuglevel = debuglevel
        self.lang = "es"
        if self.persistent_dir is None:
            try:
                import os
                if not os.path.exists(os.environ['HOME'] + "/.pydsl/"):
                    os.mkdir(os.environ['HOME'] + "/.pydsl/")
                self.persistent_dir = os.environ['HOME'] + "/.pydsl/persistent/"
                if not os.path.exists(self.persistent_dir):
                    os.mkdir(self.persistent_dir)
            except (OSError, KeyError):
                LOG.exception("Unable to create persistent dir")

    def load(self, filename):
        """Load config from file"""
        raise NotImplementedError

    def save(self):
        """Save config to file"""
        raise NotImplementedError

    @property
    def memorylist(self):
        if self.__memorylist is None:
            self.__memorylist = generate_memory_list()
        return self.__memorylist

    @property
    def debuglevel(self):
        return self.__debuglevel

    @debuglevel.setter
    def debuglevel(self, level):
        self.__debuglevel = level

GlobalConfig2 = Singleton('GlobalConfig2', (GlobalConfig, ), {})
VERSION = "pydsl pre-version\n Copyright (C) 2008-2012 Nestor Arocha"
GLOBALCONFIG = GlobalConfig2()  # The only instance available
ERRORLIST = ["Grammar", "Timeout", "Transformer"]


def all_classes(module):# -> set:
    """Returns all classes (introspection)"""
    import inspect
    result = set()
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            result.add(obj)
        elif inspect.ismodule(obj):
            if obj.__name__[:6] == "pydsl":
                result = result.union(all_classes(obj))
    return result


def all_indexable_classes(module):# -> set:
    """Returns all indexable classes (introspection)"""
    import inspect
    result = set()
    for name, obj in inspect.getmembers(module):
        from pydsl.Abstract import Indexable
        if inspect.isclass(obj) and issubclass(obj, Indexable):
            result.add(obj)
        elif inspect.ismodule(obj):
            if obj.__name__[:6] == "pydsl":
                result = result.union(all_indexable_classes(obj))
    return result
