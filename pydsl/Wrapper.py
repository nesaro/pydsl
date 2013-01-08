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

"""Wrapper Classes"""

#FIXME: python3 support only

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from abc import ABCMeta, abstractmethod, abstractproperty
from pydsl.Memory.Loader import load

class Content:
    """String wrapper"""
    def __init__(self, content):
        self.content = content
        self.grammar = None
            

    def check(self, grammar):
        return grammar in self.guess()

    def available_alphabets(self):
        return []

    def available_grammars(self):
        from pydsl.Guess import Guesser
        guess = Guesser()
        return guess(self.content)

    def select_grammar(self, grammar):
        if grammar not in self.available_grammars():
            print(self.available_grammars())
            raise Exception
        self.grammar = grammar

class FunctionsMeta(type):
    def __dir__(cls):
        from pydsl.Memory.Search.Searcher import MemorySearcher
        from pydsl.Memory.Search.Indexer import Indexer
        from pydsl.Config import GLOBALCONFIG
        searcher = MemorySearcher([Indexer(x) for x in GLOBALCONFIG.memorylist])
        return [ x["identifier"] for x in searcher.search({"ancestors":{"$in":"Function"}})]

    def __getattr__(cls, key):
        return load(key)

    @staticmethod
    def available_transforms(content):
        from pydsl.Memory.Search.Searcher import MemorySearcher
        from pydsl.Memory.Search.Indexer import Indexer
        from pydsl.Config import GLOBALCONFIG
        searcher = MemorySearcher([Indexer(x) for x in GLOBALCONFIG.memorylist])
        resultlist = []
        if content.grammar:
            grammarlist = [content.grammar]
        else:
            grammarlist = content.available_grammars()
        for element in grammarlist:
            resultlist += searcher.search({"input":{"$part":{"input":element}}})
        return [x['identifier'] for x in resultlist]

class FunctionPool(metaclass=FunctionsMeta):
    pass

class NetworkPool:
    pass

