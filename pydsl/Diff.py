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
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)


def diff(content1, content2, grammarlist = [], alphabetlist = []):
    result = {}
    if not grammarlist and not alphabetlist:
        guess1 = set(guess(content1))
        guess2 = set(guess(content2))
        grammarlist = list(guess1.union(guess2))
    for al in alphabetlist:
        tknlist1 = al.parse(content1)
        tknlist2 = al.parse(content2)
        result[al] = string_distance(tknlist1, tknlist2)
    for grammar in grammarlist:
        if is_bnf_grammar:
            tree1 = grammar.to_parse_tree(content1)
            tree2 = grammar.to_parse_tree(content2)
            diff = load_diff("tree")
            result[grammar + "_tree"] = diff(tree1, tree2)
        diff = load_diff(grammar)
        result[grammar] = diff(content1, content2)
    return result
