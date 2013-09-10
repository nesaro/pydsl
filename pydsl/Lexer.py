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
from pydsl.Memory.Loader import checker_factory
from pydsl.Alphabet.Token import Token

class AlphabetTranslator(object):
    """Translates an input written in one Alphabet into another Alphabet"""
    @property
    def input_alphabet(self):
        raise NotImplementedError

    @property
    def output_alphabet(self):
        raise NotImplementedError

class EncodingTranslator(AlphabetTranslator):
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
    """Lexer receives an Alphabet in the initialization (A1).
    Receives an input that belongs to A1 and generates a list of tokens in a different Alphabet A2
    It is always described with a regular grammar"""
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

class Tree:
    def __init__(self, content=None, index=0, parent=None):
        self.content = content
        self.parent = parent
        self.index = index
        self.children = []
        self.new = True

    def append(self, content, index):
        new = Tree(content, index, self)
        self.children.append(new)
        self.new = False
        return new

    def remove(self, element):
        self.children.remove(element)

    def __bool__(self):
        return bool(self.content)

class AlphabetListLexer(Lexer):
    def __init__(self, alphabet):
        Lexer.__init__(self)
        self.alphabet = alphabet

    @property
    def current(self):
        """Returns the element under the cursor until the end of the string"""
        return self.string[self.index:]

    def nextToken(self):
        tree = Tree()
        while tree.index < len(self.string):
            valid_alternatives = []
            index = tree.index
            for gd in self.alphabet.grammarlist:
                checker = checker_factory(gd)
                for size in range((gd.maxsize or len(self.string)) - index,
                                  max(gd.minsize-1,0),
                                  -1):
                    if checker.check(self.string[index:index+size]):
                        valid_alternatives.append((size,gd))
            if not valid_alternatives:
                if not tree: #root
                    raise Exception("Nothing consumed")
                tree.parent.remove(tree)
                tree = tree.parent
                continue
            if not tree.children and not tree.new:
                tree.parent.remove(tree)
                tree = tree.parent
                continue
            if tree.new:
                for size, gd in valid_alternatives:
                    string = self.string[index:index+size]
                    last_element = tree.append(Token(string, gd), index + size)
                    if index+size == len(self.string):
                        break
                tree = last_element
        result = []
        while tree:
            result.append(tree.content)
            tree = tree.parent
        result.reverse()
        for x in result:
            yield x

    def lexer_generator(self, target):
        next(target)
        buffer = ""
        while True:
            element = (yield)
            buffer += element #Asumes string
            for x in range(1,len(buffer)):
                currentstr = buffer[:x]
                for gd in self.alphabet.grammarlist:
                    checker = checker_factory(gd)
                    if checker.check(currentstr):
                        buffer = buffer[x:]
                        target.send(Token(currentstr, gd))


class ConceptTranslator(AlphabetTranslator):
    """Translates a set of concepts that belong to a ConceptAlphabet into another ConceptAlphabet"""
    def __init__(self, function):
        self._function = function

    def __call__(self, *args, **kwargs):
        result = self._function(*args, **kwargs)
        return result


