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

class AlphabetTranslator(object):
    @property
    def input_alphabet(self):
        raise NotImplementedError

    @property
    def output_alphabet(self):
        raise NotImplementedError

class EncodingLexer(AlphabetTranslator): #FIXME should be named EncodingAlphabetTranslator
    """Special Lexer that encodes from a string a reads a string"""
    def __init__(self, encoding):
        self.encoding = encoding

    def __call__(self, string):
        for x in string:
            yield Token(x)

    def lexer_generator(self, target):
        next(target)
        buffer = ""
        while True:
            element = (yield)
            buffer += element #Asumes string
            for x in buffer:
                target.send(Token(x))


class Lexer(AlphabetTranslator):
    """Lexer follows an alphabet definition.
    generates a list of tokens and it
    is always described with a regular grammar"""
    def __init__(self):
        self.load(None)

    @property
    def current(self):
        """Returns the element under the cursor"""
        try:
            return self.string[self.index]
        except IndexError:
            return None

    def load(self, string):
        self.string = string
        self.index = 0

    def consume(self):
        self.index += 1

    def match(self, char):
        if self.current != char:
            raise Exception("%s doesn't match %s"%(self.current,char))
        self.consume()

    def nextToken(self):
        raise NotImplementedError

    def __call__(self, string):# -> "TokenList":
        """Tokenizes input, generating a list of tokens"""
        self.string = string
        result = [x for x in self.nextToken()]
        return result

    def lexer_generator(self):
        """generator version of the lexer, yields a new token as soon as possible"""
        raise NotImplementedError

class AlphabetListLexer(Lexer):
    def __init__(self, alphabet):
        Lexer.__init__(self)
        self.alphabet = alphabet

    @property
    def current(self):
        """Returns the element under the cursor until the end of the string"""
        return self.string[self.index:]

    def nextToken(self):
        while self.current:
            validelements = []
            for gd in self.alphabet.grammarlist:
                for first_element in gd.first:
                    checker = load_checker(first_element)
                    if checker.check(self.current[0]):
                        validelements.append(gd)
                        break
            if not validelements:
                raise Exception("Not found")
            valid_alternatives = []
            for gd in validelements:
                checker = load_checker(gd)
                for size in range(gd.maxsize or len(self.current), max(gd.minsize-1,0), -1):
                    if checker.check(self.current[:size]):
                        valid_alternatives.append((size,gd))
            if not valid_alternatives:
                raise Exception("Nothing consumed", self.current)
            if len(valid_alternatives) == 1:
                size, gd = valid_alternatives[0]
                string = self.current[:size]
                for _ in range(size):
                    self.consume()
                yield Token(string, gd)
            else:
                raise Exception("Multiple choices" + str([str(x) for x in validelements]))

    def lexer_generator(self, target):
        next(target)
        buffer = ""
        while True:
            element = (yield)
            buffer += element #Asumes string
            for x in range(1,len(buffer)):
                currentstr = buffer[:x]
                for gd in self.alphabet.grammarlist:
                    checker = load_checker(gd)
                    if checker.check(currentstr):
                        buffer = buffer[x:]
                        target.send(Token(currentstr, gd))
