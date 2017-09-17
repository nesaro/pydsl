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

"""Token classes"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2017, Nestor Arocha"
__email__ = "nesaro@gmail.com"

class Token:
    def __init__(self, content, gd, left=None, right=None):
        if not gd:
            raise ValueError
        if isinstance(content, str):
            content = [x for x in content]
        self.content = content
        self.gd = gd
        self.__left = left
        self.__right = right

    def __eq__(self, other):
        return self.content == other.content and \
               self.gd == other.gd and \
               getattr(self, 'left', None) == getattr(other, 'left', None)  and \
               getattr(self, 'right', None) == getattr(other, 'right', None) 

    @property
    def left(self):
        if self.__left is None:
            raise AttributeError
        return self.__left

    @property
    def right(self):
        if self.__right is None:
            raise AttributeError
        return self.__right

    def __str__(self):
        return "".join(str(x) for x in self.content)

def append_position_to_token_list(token_list):
    """Converts a list of Token into a list of Token, asuming size == 1"""
    return [Token(value.content, value.gd, index, index+1) for (index, value) in enumerate(token_list)]


def tokenize_string(string):
    from .encoding import ascii_encoding
    return [Token(x, ascii_encoding) for x in string]

