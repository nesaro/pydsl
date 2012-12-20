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
"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"


import logging
LOG = logging.getLogger(__name__)

def validate(sgrammar, expression): # -> "[AST]":
    """Returns a list of postTreeNodes"""
    resulttrees = sgrammar.get_trees(expression, True)
    treelist = []
    for tree in resulttrees:
        from pydsl.Grammar.Tree import parser_to_post_tree
        treelist.append(parser_to_post_tree(tree))
    return treelist

