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
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pydsl.Memory.Loader import load_checker
from pydsl.Alphabet.Token import Token
finalchar = "EOF"
unknownchar = "UNKNOWN"

class AlphabetTranslator(object):
    @property
    def input_alphabet(self):
        raise NotImplementedError

    @property
    def output_alphabet(self):
        raise NotImplementedError

class EncodingLexer(AlphabetTranslator):
    """Special Lexer that encodes from a string a reads a string"""
    def __init__(self, encoding):
        self.encoding = encoding

    def __call__(self, string):
        for x in string:
            yield Token("CHAR", x)

class Lexer(AlphabetTranslator):
    """Lexer follows an alphabet definition.
    generates a list of tokens and it
    is always described with a regular grammar"""
    def __init__(self, generate_unknown=False):
        self.load(None)
        self.generate_unknown = generate_unknown

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

    def nextToken(self):
        raise NotImplementedError

    def __call__(self, string):# -> "TokenList":
        """Tokenizes input, generating a list of tokens"""
        self.string = string
        while True:
            result = [x for x in self.nextToken()]
            return result


class BNFLexer(Lexer):
    """Generates a Lexer from a BNFGrammar instance"""
    def __init__(self, bnfgrammar):
        Lexer.__init__(self)
        self.symbollist = bnfgrammar.terminalsymbollist

    @property
    def current(self):
        """Returns the element under the cursor until the end of the string"""
        try:
            return self.string[self.index:]
        except IndexError:
            return finalchar

    def nextToken(self):
        while self.current and self.current != finalchar:
            validelements = [x for x in self.symbollist if self.current[0] in x.first]
            if not validelements:
                if not self.generate_unknown:
                    raise Exception("Not found")
                string = self.current[0]
                self.consume()
                yield Token(string)
            elif len(validelements) == 1:
                element = validelements[0]
                string = self.current[:len(str(element))]
                for _ in range(len(str(element))):
                    self.consume()
                yield Token(string)
            else:
                raise Exception("Multiple choices")

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
                if not self.generate_unknown:
                    raise Exception("Not found")
                string = self.current[0]
                self.consume()
                yield Token(unknownchar, string)
            elif len(validelements) == 1:
                element = validelements[0][1]
                checker = load_checker(element)
                for size in range(element.maxsize or len(self.current), element.minsize, -1):
                    if checker.check(self.current[:size]):
                        break
                else:
                    raise Exception("Nothing consumed")
                string = self.current[:size]
                for _ in range(size):
                    self.consume()
                yield Token(validelements[0][0], string)
            else:
                raise Exception("Multiple choices")

        yield Token("EOF_TYPE", "")

