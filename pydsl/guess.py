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


""" guess which types are the input data.  """

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pydsl.check import check

class Guesser(object):
    """Returns every grammar and alphabet definition that matches the input"""
    def __init__(self, grammarlist):
        self.grammarlist = grammarlist

    def __call__(self, data):
        return [x for x in self.grammarlist if check(x,data)]

def guess(grammarlist, data):
    return Guesser(grammarlist)(data)
