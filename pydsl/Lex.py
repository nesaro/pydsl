#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is part of pydsl.
#
# pydsl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# pydsl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

"""Base Lexer classes"""
__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

from pydsl.Grammar.Alphabet import Encoding
from pydsl.Check import checker_factory
from pydsl.Config import load



class Lexer(object):

    """Translates an input written in one Alphabet into another Alphabet"""
    @property
    def input_alphabet(self):
        raise NotImplementedError

    @property
    def output_alphabet(self):
        raise NotImplementedError


class EncodingLexer(Lexer):

    """Special Lexer that encodes from a string a reads a string"""

    def __init__(self, encoding):
        self.encoding = encoding

    def __call__(self, string):
        for x in string:
            yield x

    def lexer_generator(self, target):
        next(target)
        buffer = ""
        while True:
            element = (yield)
            buffer += element  # Asumes string
            for x in buffer:
                target.send(x)


class AlphabetLexer(Lexer):

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
            raise Exception("%s doesn't match %s" % (self.current, char))
        self.consume()

    def nextToken(self):
        raise NotImplementedError

    def __call__(self, string):  # -> "TokenList":
        """Tokenizes input, generating a list of tokens"""
        self.string = string
        result = [x for x in self.nextToken()]
        return result

    def lexer_generator(self):
        """generator version of the lexer, yields a new token as soon as possible"""
        raise NotImplementedError


class AlphabetListLexer(AlphabetLexer):

    def __init__(self, alphabet):
        AlphabetLexer.__init__(self)
        self.alphabet = alphabet

    @property
    def current(self):
        """Returns the element under the cursor until the end of the string"""
        return self.string[self.index:]

    def nextToken(self):
        from pydsl.Tree import Sequence
        tree = Sequence() #This is the extract algorightm
        valid_alternatives = []
        for gd in self.alphabet.grammarlist:
            checker = checker_factory(gd)
            for left in range(0, len(self.string)):
                for right in range(left +1, len(self.string) +1 ):
                    if checker.check(self.string[left:right]):
                        valid_alternatives.append((left, right, gd))
        if not valid_alternatives:
            raise Exception("Nothing consumed")
        for left, right, gd in valid_alternatives:
            string = self.string[left:right]
            tree.append(left, right, string, check_position=False)

        right_length_seq = []
        for x in tree.generate_valid_sequences():
            if x[-1]['right'] == len(self.string):
                right_length_seq.append(x)
        for y in sorted(right_length_seq, key=lambda x:len(x))[0]: #Always gets the match with less tokens
            yield y['content']

    def lexer_generator(self, target):
        next(target)
        buffer = ""
        while True:
            element = (yield)
            buffer += element  # Asumes string
            for x in range(1, len(buffer)):
                currentstr = buffer[:x]
                for gd in self.alphabet.grammarlist:
                    checker = checker_factory(gd)
                    if checker.check(currentstr):
                        buffer = buffer[x:]
                        target.send(currentstr)


class PythonLexer(Lexer):
    """A python function based lexer"""
    def __init__(self, function):
        self._function = function

    def __call__(self, *args, **kwargs):
        result = self._function(*args, **kwargs)
        return result


def lexer_factory(alphabet):
    from pydsl.Grammar.Alphabet import Choice
    if isinstance(alphabet, str):
        alphabet = load(alphabet)
    if isinstance(alphabet, Choice):
        return AlphabetListLexer(alphabet)
    elif isinstance(alphabet, Encoding):
        return EncodingLexer(alphabet)
    else:
        raise ValueError(alphabet)

def lex(definition, data):
    return lexer_factory(definition)(data)
