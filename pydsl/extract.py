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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2017, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pydsl.check import checker_factory
from pydsl.lex import lexer_factory
from pydsl.token import PositionToken, Token


def filter_subsets(lst):
    to_remove = set()
    for i, j, _, _ in lst:
        for x, y, _, _ in lst:
            if (x < i and y >= j) or (x <= i and y > j):
                to_remove.add((i,j))
                break
    result = list(lst)

    for element in lst:
        if (element[0], element[1]) in to_remove:
            result.remove(element)
    return result


def extract_alphabet(alphabet, inputdata, fixed_start = False):
    """
    Receives a sequence and an alphabet, 
    returns a list of PositionTokens with all of the parts of the sequence that 
    are a subset of the alphabet
    """
    if not inputdata:
        return []
    base_alphabet = alphabet.alphabet

    lexer = lexer_factory(alphabet, base_alphabet)
    totallen = len(inputdata)
    maxl = totallen
    minl = 1
    if fixed_start:
        max_start = 1
    else:
        max_start = totallen
    result = []
    for i in range(max_start):
        for j in range(i+minl, min(i+maxl, totallen) + 1):
            try:
                lexed = lexer(inputdata[i:j])
                if lexed and len(lexed) == 1:
                    result.append((i,j, inputdata[i:j], lexed[0].gd))
                elif lexed:
                    raise Exception
            except:
                continue
    result = filter_subsets(result)
    return [PositionToken(content, gd, left, right) for (left, right, content, gd) in result]

def extract(grammar, inputdata, fixed_start = False, return_first=False):
    """
    Receives a sequence and a grammar, 
    returns a list of PositionTokens with all of the parts of the sequence that 
    are recognized by the grammar
    """
    if not inputdata:
        return []
    checker = checker_factory(grammar)

    totallen = len(inputdata)
    from pydsl.grammar.PEG import Choice
    try:
        maxl = grammar.maxsize or totallen
    except NotImplementedError:
        maxl = totallen
    try:
        #minl = grammar.minsize #FIXME: It won't work with incompatible alphabets
        minl = 1
    except NotImplementedError:
        minl = 1
    if fixed_start:
        max_start = 1
    else:
        max_start = totallen
    result = []
    for i in range(max_start):
        for j in range(i+minl, min(i+maxl, totallen) + 1):
            slice = inputdata[i:j]
            check = checker.check(slice)
            if check:
                this_pt = PositionToken(slice, grammar, i, j)
                if return_first:
                    return this_pt
                result.append(this_pt)
    return result

def search(grammar, inputdata):
    return extract(grammar, inputdata, return_first=True)

def match(grammar, inputdata):
    return extract(grammar, inputdata, fixed_start=True, return_first=True)

