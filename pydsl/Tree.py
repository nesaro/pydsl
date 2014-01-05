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


class ParseTree(object):

    """Stores the position of the original tree"""

    def __init__(self, leftpos, rightpos, symbol, content, childlist=None, valid=True):
        self.symbol = symbol
        if not isinstance(leftpos, int) and leftpos is not None:
            raise TypeError
        if not isinstance(rightpos, int) and rightpos is not None:
            raise TypeError
        if not childlist:
            childlist = []
        self.childlist = childlist
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

    def append(self, dpr):
        """appends dpr to childlist"""
        self.childlist.append(dpr)


class Sequence:
    def __init__(self):
        self.possible_items = []

    @property
    def current_right(self):
        if not self.possible_items:
            return set([0])
        return set(x['right'] for x in self.possible_items)

    def append(self, left, right, content, gd = None, check_position=True):
        if left > right:
            raise ValueError('Attempted to add negative length alement')
        if check_position == True and left:
            if left not in self.current_right:
                raise ValueError("Unable to add element")
        result = {'left':left, 'right':right, 'content':content}
        if gd:
            result['gd'] = gd
        self.possible_items.append(result)

    def valid_sequences(self):
        """Returns list"""
        valid_sets = [[x] for x in self.possible_items if x['left'] == 0]
        change = True
        niter = 200
        while change and niter > 0:
            change = False
            niter -=1
            for possible in self.possible_items:
                for current_valid in valid_sets[:]:
                    if possible['left'] == current_valid[-1]['right']:
                        if current_valid + [possible] not in valid_sets:
                            if current_valid[-1]['left'] != current_valid[-1]['right'] or possible['left'] != possible['right']: #avoids Null insertion twice
                                valid_sets.append(current_valid + [possible])
                                change = True
        if not niter:
            raise Exception('too many iterations')
        return valid_sets

    def right_limit_list(self):
        if not self.possible_items:
            return [0]
        return list(set([x[-1]['right'] for x in self.valid_sequences()]))


