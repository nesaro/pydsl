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
from pydsl.Factory import checker_factory


__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"
#FIXME: Use globalconfig memory list
#TODO: Add Alphabet support


import logging
LOG = logging.getLogger(__name__)
from pydsl.Alphabet.Definition import AlphabetDefinition
from pydsl.Grammar.Definition import GrammarDefinition

def extract(grammar, inputdata):
    """Extract every slice of the input data that belongs to the Grammar Definition"""
    checker = checker_factory(grammar)
    totallen = len(inputdata)
    if isinstance(grammar, GrammarDefinition):
        try:
            maxl = grammar.maxsize or totallen
        except NotImplementedError:
            maxl = totallen
        try:
            minl = grammar.minsize
        except NotImplementedError:
            minl = 1
    elif isinstance(grammar, AlphabetDefinition):
        maxl = totallen
        minl = 1
    else:
        raise TypeError
    maxwsize = maxl - minl + 1
    result = []
    for i in range(totallen):
        for j in range(i+minl, min(i+maxwsize+1, totallen+1)):
            check = checker.check(inputdata[i:j])
            if check:
                result.append((i,j, inputdata[i:j]))
    return result

