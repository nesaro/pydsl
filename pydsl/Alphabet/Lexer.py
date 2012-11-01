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

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2012, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from abc import ABCMeta, abstractmethod, abstractproperty
from pydsl.Memory.Loader import load_checker
finalchar = "EOF"

###Lexer follows an alphabet definition, which is like a grammar definition but generates a list of tokens and it is always Readable using a regular grammar

class Lexer(metaclass=ABCMeta):
    def __init__(self):
        self.string = None
        self.index = 0

    @property
    def current(self):
        """Returns the element under the cursor"""
        try:
            return self.string[self.index]
        except IndexError:
            return finalchar

    def load(self, string):
        self.string = string
        self.index = 0

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

    def __call__(self, string) -> "TokenList":
        """Tokenizes input, generating a list of tokens"""
        self.string = string
        result = []
        while True:
            nt = self.nextToken()
            result.append(nt)
            if nt[0] == "EOF_TYPE":
                return result


class BNFLexer(Lexer):
    """Generates a Lexer from a BNFGrammar instance"""
    def __init__(self, bnfgrammar):
        Lexer.__init__(self)
        self.symbollist = bnfgrammar.getTerminalSymbols()

    @property
    def current(self):
        """Returns the element under the cursor until the end of the string"""
        try:
            return self.string[self.index:]
        except IndexError:
            return finalchar

    def nextToken(self):
        import re
        while self.current != finalchar:
            validelements = [x for x in self.symbollist if self.current[0] in x.first]
            if not validelements:
                raise Exception("Not found")
            if len(validelements) == 1:
                element = validelements[0]
                string = self.current[:len(element)]
                for _ in range(len(element)):
                    self.consume()
                return (validelements[0].name, string)
            else:
                raise Exception("Multiple choices")

        return ("EOF_TYPE", "")

class AlphabetDictLexer(Lexer):
    def __init__(self, alphabet):
        Lexer.__init__(self)
        self.alphabet = alphabet

    @property
    def current(self):
        """Returns the element under the cursor until the end of the string"""
        try:
            return self.string[self.index:]
        except IndexError:
            return finalchar

    def nextToken(self):
        while self.current:
            validelements = [(x,y) for x,y in self.alphabet.grammardict.items() if self.current[0] in y.first]
            if not validelements:
                raise Exception("Not found")
            if len(validelements) == 1:
                element = validelements[0][1]
                size = 0
                checker = load_checker(element)
                for size in range(element.maxsize or len(self.current), element.minsize, -1):
                    if checker.check(self.current[:size]):
                        break
                else:
                    raise Exception("Nothing consumed")
                string = self.current[:size]
                for _ in range(size):
                    self.consume()
                return (validelements[0][0], string)
            else:
                raise Exception("Multiple choices")

        return ("EOF_TYPE", "")

