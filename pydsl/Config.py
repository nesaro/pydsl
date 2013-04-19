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

from pydsl.Abstract import Singleton
import logging
LOG = logging.getLogger(__name__)
from pkg_resources import resource_filename

def load_default_memory():
    from pydsl.Memory.Directory import DirStorage
    from pydsl.Memory.Dict import RegexpDictStorage
    from pydsl.Memory.List import EncodingStorage
    dirname = resource_filename("pydsl.contrib", "")
    GLOBALCONFIG.memorylist.append(DirStorage(dirname + "/grammar/"))
    GLOBALCONFIG.memorylist.append(RegexpDictStorage(dirname + "/dict/regexp.dict"))
    GLOBALCONFIG.memorylist.append(EncodingStorage(dirname + "/list/encoding.py"))
    GLOBALCONFIG.memorylist.append(DirStorage(dirname + "/transformer/"))

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
    def __init__(self, persistent_dir=None, debuglevel=40):
        self.persistent_dir = persistent_dir
        self.memorylist = []
        self.formatlist = default_formats()
        self.__debuglevel = debuglevel
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
    def debuglevel(self):
        return self.__debuglevel

    @debuglevel.setter
    def debuglevel(self, level):
        self.__debuglevel = level

GlobalConfig2 = Singleton('GlobalConfig2', (GlobalConfig, ), {})
GLOBALCONFIG = GlobalConfig2()  # The only instance available
