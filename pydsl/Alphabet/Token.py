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


class Token(object):
    """ Stores a symbol and its associated input """
    def __init__(self, terminalsymbol, string):
        self.symbol = terminalsymbol
        self.string = string

    def __str__(self):
        return self.string

class TokenList(list):
    def __bool__(self):
        return len(self) > 1

    def __str__(self):
        return "".join([str(x[1]) for x in self[:-1]])

