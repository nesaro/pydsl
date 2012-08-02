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

"""Grammar FileLibraries"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"


import logging
LOG = logging.getLogger(__name__)
from .Python import getFileTuple

def _isGDLFileName(path):
    return path.endswith(".bnf")

def _isRELFileName(path):
    return path.endswith(".re")

def load_grammar_file(filepath):
    if _isRELFileName(filepath):
        from pydsl.Memory.Storage.File.Regexp import load_re_from_file
        return load_re_from_file(filepath)
    if _isGDLFileName(filepath):
        from pydsl.Memory.Storage.File.BNF import load_bnf_file
        return load_bnf_file(filepath)
    from .Python import load_python_file 
    return load_python_file(filepath)
    

