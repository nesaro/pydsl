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


"""Regular expression file parser"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"


import re

def load_re_from_file(filepath):
    """Converts a re file to Regular Grammar instance"""
    regexp = None
    with open(filepath,'r') as mlfile:
        flagstr = ""
        for line in mlfile:
            cleanline = re.sub("//.*$", "", line)
            if re.search("^\s*$", cleanline):
                continue
            if re.search ("^#.*$", cleanline):
                flagstr = cleanline[1:]
                continue
            if regexp is not None:
                raise Exception("Regular expression file format error")
            else:
                regexp = cleanline.rstrip('\n')
    flags = 0
    if "i" in flagstr:
        flags |= re.I
    from pydsl.grammar.definition import RegularExpression
    return RegularExpression(regexp, flags)
