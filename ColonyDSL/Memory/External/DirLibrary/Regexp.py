#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of ColonyDSL.
#
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


"""Regular expression file parser"""

__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


import logging

import re
LOG = logging.getLogger("Regexp")

def colonyRELfileToGrammarInstance(filepath):
    """Converts a re file to Regular Grammar instance"""
    regexp = None
    from ColonyDSL.Memory.External.DirLibrary.DirLibrary import getFileTuple
    with open(filepath,'r', encoding='utf-8') as mlfile:
        flagstr = ""
        for line in mlfile:
            cleanline = re.sub("//.*$", "", line)
            if re.search("^\s*$", cleanline):
                continue
            if re.search ("^#.*$", cleanline):
                flagstr = cleanline[1:]
                continue
            if regexp != None: 
                LOG.error("Regular expression file format error")
                raise Exception #TODO find proper exception
            else:
                regexp = cleanline.rstrip('\n')
    from ColonyDSL.Type.Grammar.Regular import RegularExpressionGrammar
    return RegularExpressionGrammar(regexp, flagstr)

