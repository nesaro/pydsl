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

"""Base Lexer classes"""

__author__ = "Nestor Arocha Rodriguez"
__copyright__ = "Copyright 2008-2012, Nestor Arocha Rodriguez"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from abc import ABCMeta, abstractmethod, abstractproperty
finalchar = "EOF"

class Lexer(metaclass = ABCMeta):
    def __init__(self):
        self.string = None
        self.index = 0

    @property
    def current(self):
        try:
            return self.string[self.index]
        except IndexError:
            return finalchar

    def consume(self):
        self.index += 1

    def match(self, char):
        if self.current == char:
            self.consume()
        else:
            raise Exception

    @abstractmethod
    def nextToken(self):
        pass

    @abstractmethod
    def __call__(self, string) -> "TokenList":
        """Tokenizes input, generating a list of tokens"""
        pass

class BNFLexer(Lexer):
    def __init__(self, bnfgrammar, string = ""):
        Lexer.__init__(self, string)

    def nextToken(self):
        import re
        from pydsl.Grammar.Lexer import finalchar
        while self.current != finalchar:
            if self.current == "/":
                self.comment(tl)
                continue
            elif self.current == " ":
                self.consume()
                continue
            elif self.current == ",":
                return self.comma()
            elif self.current == "[":
                return self.lbrack()
            elif self.current == "]":
                return self.rbrack()
            elif re.match("[a-zA-Z]", self.current):
                return self.name()
            else:
                raise Exception
        return ("EOF_TYPE", "")

    def comma(self):
        current = self.current
        self.match(",")
        return ("COMMA", current)

    def lbrack(self):
        current = self.current
        self.match("[")
        return ("LBRACK", current)

    def rbrack(self):
        current = self.current
        self.match("]")
        return ("RBRACK", current)

    def name(self):
        import re
        string = ""
        from pydsl.Grammar.Lexer import finalchar
        while self.current != finalchar and re.match("[a-zA-Z]", self.current):
            string += self.current
            self.consume()
        return ("NAME", string)

