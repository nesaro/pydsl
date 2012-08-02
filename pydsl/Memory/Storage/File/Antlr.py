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


"""ANLTr grammar format functions"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pydsl.Grammar.Lexer import BacktracingLexer

#manual lexer

reservedwords = ["grammar","options","language","output","ASTLabelType",":",";","|","*"]

comments = ["/**/"]

class ANLTRGrammarLexer(BacktracingLexer):
    def comma(self):
        current = self.current
        self.match(",")
        return ("COMMA", current)

    def colon(self):
        current = self.current
        self.match(":")
        return ("COLON", current)

    def vbar(self):
        current = self.current
        self.match("|")
        return ("VBAR", current)

    def __call__(self):
        if self.speculate_stat_1():
            self.rlist()
            self.match("EOF_TYPE")
        elif self.speculate_stat_2():
            self.assign()
            self.match("EOF_TYPE")
        else:
            raise Exception("No alternative for stat")
        

def load_anltr_from_text(text):
    lexer = ANLTRGrammarLexer()
    return lexer(text)


#manual parser
def load_anltr_file(filepath):
    """Converts an anltr .g file into a BNFGrammar instance"""
    content = ""
    with open(filepath,'r', encoding='utf-8') as mlfile:
        content = mlfile.read()

    
