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

    def __init__(self, leftpos, rightpos, content, production=None, valid=True, childlist=None):
        Tree.__init__(self, childlist)
        self.leftpos = leftpos
        self.rightpos = rightpos
        self.content = content
        self.valid = valid
        self.production = production

    def __eq__(self, other):
        try:
            return self.production == other.production and self.content == other.content and self.leftpos == other.leftpos and self.rightpos == other.rightpos and self.valid == other.valid
        except AttributeError:
            return False

    def __bool__(self):
        """checks if it is a null result"""
        return self.valid

    def __getitem__(self, key):
        result = []
        mylist = self.to_list(order)
        for element in mylist:
            if element.content == key:
                result.append(element)
        if not result:
            raise KeyError("Element not found %s" % key)
        return result

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

    def coverage(self):
        if not self:
            return 0, len(self)
        if self.childlist:
            childtotal = 0
            childcoverage = 0
            for child in self.childlist:
                newcoverage, newtotal = child.coverage()
                childcoverage += newcoverage
                childtotal += newtotal
            assert(childtotal == len(self))
            return childcoverage, childtotal
        else:
            return len(self), len(self)

    def get_by_symbol(self, index):
        if isinstance(self.production, TerminalSymbol):
            # FIXME quick hack for terminal rules
            return [(self.leftpos, self.rightpos)]
        result = []
        if self.production.leftside[0].name == index:
            result.append((self.leftpos, self.rightpos))
        else:
            LOG.debug(
                "Not equal: " + str(self.production.leftside[0].name) + " and :" + str(index))
        for child in self.childlist:
            result += child.get_by_symbol(index)
        return result

    def __contains__(self, index):
        if isinstance(self.production, TerminalSymbol):
            # FIXME quick hack for terminal rules
            return index == self.production.name
        if not self.production.leftside:
            return False
        if self.production.leftside[0].name == index:
            return True
        for child in self.childlist:
            if child.get_by_symbol(index):
                return True
        return False


class ParseTree(PositionTree):

    """ Stores a descent parser iteration result """

    def __init__(self, leftpos, rightpos, symbollist, content, production, childlist=None, valid=True):
        if not isinstance(leftpos, int) and leftpos is not None:
            raise TypeError
        if not isinstance(rightpos, int) and rightpos is not None:
            raise TypeError
        if not isinstance(symbollist, list):
            raise TypeError
        from pydsl.Grammar.BNF import Production
        if production is not None and not (isinstance(production, (Production, TerminalSymbol))):
            raise TypeError(production)
        PositionTree.__init__(
            self, leftpos, rightpos, content, production, valid, childlist)
        self.symbollist = symbollist

    def __add__(self, other):
        """ Adds two results. Only if self.rightpos = other.leftpos and parents are the same """
        if not isinstance(other, ParseTree):
            raise TypeError
        if other == []:
            return ParseTree(self.leftpos, self.rightpos, self.symbollist,
                             self.content, self.production, self.childlist)  # FIXME: Must return a childlist copy
        if self.rightpos == other.leftpos and self.production == other.production:
            leftpos = self.leftpos
            rightpos = other.rightpos
            production = self.production
            content = self.content + other.content
            symbollist = self.symbollist + other.symbollist
            childlist = self.childlist + other.childlist
            return ParseTree(leftpos, rightpos, symbollist, content, production, childlist)
        else:
            LOG.warning("Unable to add parser results")
            raise Exception

