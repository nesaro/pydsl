#!/usr/bin/python
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
__copyright__ = "Copyright 2008-2020, Nestor Arocha"
__email__ = "n@nestorarocha.com"

import logging
from collections import Iterable
from .check import check
from jsonschema import FormatChecker
LOG = logging.getLogger(__name__)

def equal(definition, first_element, second_element) -> bool:
    """Compares if the two elements are equal according to the grammar definition"""
    if not check(definition, first_element):
        raise ValueError
    if not check(definition, second_element):
        raise ValueError
    equal_checker = equal_factory(definition)
    return equal_checker(first_element, second_element)


def equal_factory(definition):
    from pydsl.grammar.definition import String
    if isinstance(definition, String):
        return lambda x,y: x==y

