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
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)


class ParseTree(object):

    """Stores the position of the original tree"""

    def __init__(self, left, right, symbol, content, childlist=None, valid=True):
        self.symbol = symbol
        if not isinstance(left, int) and left is not None:
            raise TypeError
        if not isinstance(right, int) and right is not None:
            raise TypeError
        self.childlist = childlist or []
        self.left = left
        self.right = right
        self.content = content
        self.valid = valid

    def __eq__(self, other):
        try:
            return self.left == other.left and self.right == other.right and self.valid == other.valid and self.content == other.content 
        except AttributeError:
            return False

    def __bool__(self):
        """checks if it is a null result"""
        return self.valid

    def __nonzero__(self):
        return self.__bool__()

    def shift(self, amount):
        """ shifts position """
        if self.left is not None:
            self.left += amount
        if self.left is not None:
            self.right += amount

    def __len__(self):
        if self.right is None and self.left is None:
            return 0
        return self.right - self.left

    def append(self, dpr):
        """appends dpr to childlist"""
        self.childlist.append(dpr)


class PositionResultList(object):
    """Contains a list of results"""
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
        if check_position and left and left not in self.current_right:
            raise ValueError("Unable to add element")
        result = {'left':left, 'right':right, 'content':content}
        if gd:
            result['gd'] = gd
        self.possible_items.append(result)

    def valid_sequences(self):
        positions = set((x['left'], x['right']) for x in self.possible_items)
        max_right = max(x[1] for x in positions)
        sorted_entries = sorted(positions, key= lambda x:x[0])

        class RTree:
            def __init__(self, content):
                self.content = content
                self.childrenset = set()

            @property
            def children(self):
                return [node_cache[x] for x in self.childrenset if x in node_cache]

            @property
            def max_length(self):
                if self.children:
                    return 1 + max(x.max_length for x in self.children)
                return 1

            @property
            def min_length(self):
                if self.children:
                    return 1 + min(x.min_length for x in self.children)
                return 1

            @property
            def shortest_flat_tree(self):
                if not self.childrenset:
                    return [self.content]
                shortest_child = min((x for x in self.children), key=lambda x: x.min_length)
                return [self.content] + shortest_child.shortest_flat_tree
    
            def generate_content(self):
                if not self.children:
                    yield [self.content]
                else:
                    for x in self.children:
                        child_result = list(x.generate_content())
                        result = [self.content] + child_result[0]
                        yield result

            def get_or_create_child(self, value):
                if not isinstance(value, int):
                    raise ValueError
                self.childrenset.add(value)
                if value not in node_cache:
                    new_tree = RTree(value)
                    node_cache[value] = new_tree
                return node_cache[value]

        def clean(value):
            print("clean {}".format(value))
            print([(x,y.childrenset) for x,y in node_cache.items()])
            for x in range(value-1, 0, -1):
                if x not in node_cache:
                    continue
                for y in range(x):
                    if y not in node_cache:
                        continue
                    if x in node_cache[y].childrenset:
                        break
                else:
                    print("removing {}".format(x))
                    del node_cache[x]


        starting_tree = RTree(0)
        from collections import defaultdict
        node_cache = {}
        node_cache[0] = starting_tree
    
        def add_node(left, right):
            if left > right:
                return
            print("adding {} {}".format(left, right))
            if left not in node_cache:
                node_cache[left] = RTree(left)
            node_cache[left].get_or_create_child(right)

        last_left = 0
        for index in range(len(sorted_entries)):
            print(index)
            left, right = sorted_entries[index]
            if left != last_left:
                clean(last_left)
                last_left = left
            add_node(left, right)
        #starting_tree.clean(max_right)
        
        def convert_back(flat_list):
            print("CONVERT {}".format(flat_list))
            for x in range(len(flat_list) - 1):
                left, right = flat_list[x:x+2]
                print((left,right))
                for element in self.possible_items:
                    if element['left'] == left and element['right'] == right:
                        #print(element)
                        yield element
                        break

        #yield from starting_tree.generate_content()
        return [list(convert_back(y)) for y in starting_tree.generate_content()]


    def right_limit_list(self):
        if not self.possible_items:
            return [0]
        return list(set([x[-1]['right'] for x in self.valid_sequences()]))


