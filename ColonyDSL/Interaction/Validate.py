#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of ColonyDSL.
#
#ColonyDSL is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#ColonyDSL is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with ColonyDSL.  If not, see <http://www.gnu.org/licenses/>.


"""
"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


import logging
LOG = logging.getLogger("Validate")

def validate(sgrammar:"SymbolGrammar", expression) -> "[PostTreeNode]":
    """Returns a list of postTreeNodes"""
    resulttrees = sgrammar.get_trees(expression, True)
    treelist = []
    for tree in resulttrees:
        from ColonyDSL.Type.Grammar.Tree import parser_to_post_tree
        treelist.append(parser_to_post_tree(tree))
    return treelist

