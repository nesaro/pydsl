#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Néstor Arocha Rodríguez
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

"""WeightedParser"""

import logging
LOG = logging.getLogger(__name__)
from .Parser import TopDownParser

def locate_heavier_symbol(symbollist):
    """ Locates the heavier symbol inside inputlist"""
    currentsymbol = None
    for symbol in symbollist:
        if currentsymbol == None or symbol.weight > currentsymbol.weight:
            currentsymbol = symbol
    return currentsymbol

class WeightedParser(TopDownParser):
    """Weighted Parser class"""
    pass
