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
    def __init__(self, content, gd):
        if not gd:
            raise ValueError
        if isinstance(content, str):
            content = [x for x in content]
        elif isinstance(content[0], Token):
            content = [str(x) for x in content]
        self.content = content
        self.gd = gd

    def __eq__(self, other):
        try:
            return self.content == other.content and \
                   self.gd == other.gd
        except AttributeError:
            return False

    def __str__(self):
        return "".join(str(x) for x in self.content)

class PositionToken(Token):
    def __init__(self, content, gd, left=None, right=None):
        super().__init__(content, gd)
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.content == other.content and \
               self.gd == other.gd and \
               self.left == other.left and \
               self.right == other.right
               

    def __str__(self):
        return "".join(str(x) for x in self.content)


def append_position_to_token_list(token_list):
    """Converts a list of Token into a list of Token, asuming size == 1"""
    return [PositionToken(value.content, value.gd, index, index+1) for (index, value) in enumerate(token_list)]


def tokenize_string(string):
    from .encoding import ascii_encoding
    return [Token(x, ascii_encoding) for x in string]

