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
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pkg_resources import resource_filename

def load_default_memory():
    from pydsl.Memory.Dict import RegexpDictStorage
    from pydsl.Memory.List import EncodingStorage
    from pypository.Directory import DirStorage
    from regexps import res
    dirname = resource_filename("pydsl.contrib", "")
    GLOBALCONFIG.memorylist.append(DirStorage(dirname + "/grammar/", GLOBALCONFIG.formatlist))
    GLOBALCONFIG.memorylist.append(DirStorage(dirname + "/alphabet/", GLOBALCONFIG.formatlist))
    GLOBALCONFIG.memorylist.append(RegexpDictStorage(res))
    GLOBALCONFIG.memorylist.append(EncodingStorage(dirname + "/encoding.py"))
    GLOBALCONFIG.memorylist.append(DirStorage(dirname + "/transformer/", GLOBALCONFIG.formatlist))

def default_formats():
    from pydsl.Memory.File.Regexp import load_re_from_file, summary_re_from_file
    from pydsl.Memory.File.BNF import load_bnf_file, summary_bnf_file
    from pydsl.Memory.File.Python import summary_python_file, load_python_file
    return [
        {"extension":".py",  "summary_from_file":summary_python_file, "load_from_file":load_python_file},
        {"extension":".re", "summary_from_file":summary_re_from_file,"load_from_file":load_re_from_file},
        {"extension":".bnf","summary_from_file":summary_bnf_file, "load_from_file":load_bnf_file},
        ]

class GlobalConfig(object):
    """Execution time global configuration"""
    def __init__(self, debuglevel=40):
        self.memorylist = []
        self.formatlist = default_formats()
        self.__debuglevel = debuglevel

    def load(self, filename):
        """Load config from file"""
        raise NotImplementedError

    def save(self):
        """Save config to file"""
        raise NotImplementedError

    @property
    def debuglevel(self):
        return self.__debuglevel

    @debuglevel.setter
    def debuglevel(self, level):
        self.__debuglevel = level

class Singleton(type):
    """singleton pattern metaclass"""
    #Only problem here is that classes can't have two metaclasses
    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)

    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args, **kw)
        return cls.__instance

GlobalConfig2 = Singleton('GlobalConfig2', (GlobalConfig, ), {})
GLOBALCONFIG = GlobalConfig2()  # The only instance available
