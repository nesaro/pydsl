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


"""Abstract Classes"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from abc import ABCMeta, abstractmethod
from pydsl.Abstract import Indexable

class Checker(metaclass = ABCMeta):
    """ Ensures information follows a rule, protocol or has a shape.
    Provides only check function, for complex operations, use Grammar"""
    @abstractmethod
    def check(self, value) -> bool:
        pass

class DummyChecker(Checker):
    """Always True Checker"""
    def check(self, word):
        return True
        
    def __eq__(self, other):
        if isinstance(other, DummyChecker):
            return True
        return False
        
class RegularExpressionChecker(Checker):
    def __init__(self, regexp, flags = ""):
        import re
        self.__regexpstr = regexp
        myflags = 0
        if "i" in flags:
            myflags |= re.I
        if isinstance(regexp, str):
            self.__regexp = re.compile(regexp, myflags)
        else:
            self.__regexp = regexp

    def check(self, word):
        """returns True if any match any regexp"""
        try:
            data = str(word)
        except UnicodeDecodeError:
            return False
        if data == "":
            return False
        if self.__regexp.match(data):
            return True
        return False

