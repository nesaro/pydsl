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


"""
guess which types are the input data. 
"""
from pydsl.Checker import check

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"
#TODO: Add Alphabet support


import logging
LOG = logging.getLogger(__name__)
from pkg_resources import resource_filename
from pypository.search.Searcher import Searcher
from pydsl.Config import GLOBALCONFIG


class Guesser(object):
    """Returns every grammar and alphabet definition that matches the input"""
    def __init__(self, memorylist = None):
        if not memorylist:
            memorylist = GLOBALCONFIG.memorylist
        self.memorylist = memorylist
        self.searcher = Searcher([x.indexer for x in memorylist])

    def __call__(self, inputstring): #-> set:
        result = set()
        for summary in self.searcher.search():
            try:
                for mem in self.memorylist:
                    if summary["identifier"] in mem:
                        name = summary["identifier"]
                        try:
                            typ = mem.load(name)
                        except:
                            LOG.warning("Error while loading memory %s" % name)
                            continue
                        break
                else:
                    continue # not found 
                if check(typ, inputstring):
                    result.add(str(name))
            except (TypeError, ValueError):
                continue
        return result
