#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is part of pydsl.
#
# pydsl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# pydsl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

"""Tree class for tree based parsers"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pydsl.Grammar.Symbol import TerminalSymbol


def traversePreOrder(item):
    result = [item]
    for child in item.childlist:
        result += traversePreOrder(child)
    return result


def traverseInOrder(item):
    result = [traverseInOrder(item.childlist[0]), item]
    for child in item.childlist[1:]:
        result += traverseInOrder(child)
    return result


def traversePostOrder(item):
    result = []
    for child in item.childlist:
        result += traversePostOrder(child)
    result.append(item)
    return result


class Tree(object):

    def __init__(self, childlist=None):
        if not childlist:
            childlist = []
        self.childlist = childlist

    def append_child(self, dpr):
        """appends dpr to childlist"""
        self.childlist.append(dpr)

    def to_list(self, order="preorder"):
        if order == "preorder":
            return traversePreOrder(self)
        elif order == "inorder":
            return traverseInOrder(self)
        elif order == "postorder":
            return traversePostOrder(self)
        else:
            raise ValueError("Unknown order %s" % order)

    def first_leaf(self):
        """Returns the first lead node"""
        if self.childlist:
            return self.childlist[0].first_leaf()
        else:
            return self


class PositionTree(Tree):

    """Stores the position of the original tree"""

    def __init__(self, leftpos, rightpos, content, valid=True, childlist=None):
        Tree.__init__(self, childlist)
        self.leftpos = leftpos
        self.rightpos = rightpos
        self.content = content
        self.valid = valid

    def __eq__(self, other):
        try:
            return self.leftpos == other.leftpos and self.rightpos == other.rightpos and self.valid == other.valid and self.content == other.content 
        except AttributeError:
            return False

    def __bool__(self):
        """checks if it is a null result"""
        return self.valid

    def shift(self, amount):
        """ shifts position """
        if self.leftpos is not None:
            self.leftpos += amount
        if self.leftpos is not None:
            self.rightpos += amount

    def __len__(self):
        if self.rightpos is None and self.leftpos is None:
            return 0
        return self.rightpos - self.leftpos


class ParseTree(PositionTree):

    """ Stores a descent parser iteration result """

    def __init__(self, leftpos, rightpos, symbollist, content, childlist=None, valid=True):
        if not isinstance(leftpos, int) and leftpos is not None:
            raise TypeError
        if not isinstance(rightpos, int) and rightpos is not None:
            raise TypeError
        if not isinstance(symbollist, list):
            raise TypeError
        from pydsl.Grammar.BNF import Production
        PositionTree.__init__(self, leftpos, rightpos, content, valid, childlist)
        self.symbollist = symbollist


class Sequence:
    def __init__(self):
        self.possible_items = []

    @property
    def current_right(self):
        if not self.possible_items:
            return set([0])
        return set(x['right'] for x in self.possible_items)

    def append(self, left, right, content, check_position=True):
        if left > right:
            raise Exception
        if check_position == True and left:
            if left not in self.current_right:
                raise ValueError("Unable to add element")
        self.possible_items.append({'left':left, 'right':right, 'content':content})

    def generate_valid_sequences(self):
        """Returns list"""
        valid_sets = [[x] for x in self.possible_items if x['left'] == 0]
        change = True
        while change:
            change = False
            for possible in self.possible_items:
                for current_valid in valid_sets[:]:
                    if possible['left'] == current_valid[-1]['right']:
                        if current_valid + [possible] not in valid_sets:
                            if possible['content'] != current_valid[-1]['content']:
                                valid_sets.append(current_valid + [possible])
                                change = True
        return valid_sets

    def right_limit_list(self):
        if not self.possible_items:
            return [0]
        return list(set([x[-1]['right'] for x in self.generate_valid_sequences()]))


