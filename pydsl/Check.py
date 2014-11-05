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


__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2014, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
from collections import Iterable
LOG = logging.getLogger(__name__)


def check(definition, data):
    checker = checker_factory(definition)
    return checker(data)

def checker_factory(grammar):
    from pydsl.Grammar.BNF import BNFGrammar
    from pydsl.Grammar.PEG import Sequence, Choice, OneOrMore, ZeroOrMore
    from pydsl.Grammar.Definition import PLYGrammar, RegularExpression, String, PythonGrammar, JsonSchema
    from pydsl.Grammar.Parsley import ParsleyGrammar
    if isinstance(grammar, str) and not isinstance(grammar, String):
        raise TypeError(grammar)
    if isinstance(grammar, BNFGrammar):
        return BNFChecker(grammar)
    elif isinstance(grammar, JsonSchema):
        return JsonSchemaChecker(grammar)
    elif isinstance(grammar, RegularExpression):
        return RegularExpressionChecker(grammar)
    elif isinstance(grammar, PythonGrammar) or isinstance(grammar, dict) and "matchFun" in grammar:
        return PythonChecker(grammar)
    elif isinstance(grammar, PLYGrammar):
        return PLYChecker(grammar)
    elif isinstance(grammar, Choice):
        return ChoiceChecker(grammar)
    elif isinstance(grammar, ParsleyGrammar):
        return ParsleyChecker(grammar)
    elif isinstance(grammar, String):
        return StringChecker(grammar)
    elif isinstance(grammar, Sequence):
        return SequenceChecker(grammar)
    elif isinstance(grammar, OneOrMore):
        return OneOrMoreChecker(grammar)
    elif isinstance(grammar, ZeroOrMore):
        return ZeroOrMoreChecker(grammar)
    elif isinstance(grammar, Iterable):
        return ChoiceChecker(grammar)
    else:
        raise ValueError(grammar)


class Checker(object):
    """ Ensures that input follows a rule, protocol, grammar alphabet..."""
    def __init__(self):
        pass

    def __call__(self, value):
        return self.check(value)

    def check(self, value):# -> bool:
        raise NotImplementedError

    def _normalize_input(self, data):
        result = []
        for x in data:
            from pydsl.Token import Token, PositionToken
            if isinstance(x, (Token, PositionToken)):
                result.append(x.content)
            else:
                result.append(x)
        return result

class RegularExpressionChecker(Checker):
    def __init__(self, regexp, flags = ""):
        Checker.__init__(self)
        import re
        self.__regexpstr = regexp
        myflags = 0
        if "i" in flags:
            myflags |= re.I
        if isinstance(regexp, str):
            self.__regexp = re.compile(regexp, myflags)
        else:
            self.__regexp = regexp

    def check(self, data):
        """returns True if any match any regexp"""
        if isinstance(data, Iterable):
            data = "".join([str(x) for x in data])
        try:
            data = str(data)
        except UnicodeDecodeError:
            return False
        return bool(data and self.__regexp.match(data))


class BNFChecker(Checker):
    """Calls another program to perform checking. Args are always file names"""
    def __init__(self, bnf, parser = None):
        Checker.__init__(self)
        self.gd = bnf
        parser = bnf.options.get("parser",parser)
        if parser in ("descent", "auto", "default", None):
            from pydsl.Parser.Backtracing import BacktracingErrorRecursiveDescentParser
            self.__parser = BacktracingErrorRecursiveDescentParser(bnf)
        else:
            raise ValueError("Unknown parser : " + parser)

    def check(self, data):
        for element in data:
            if not check(self.gd.alphabet, element):
                LOG.warning("Invalid input: %s,%s" % (self.gd.alphabet, element))
                return False
        try:
            return len(self.__parser.get_trees(data)) > 0
        except IndexError:
            return False 

class ParsleyChecker(Checker):
    def __init__(self, grammar):
        Checker.__init__(self)
        self.gd=grammar

    def check(self, data):
        from parsley import ParseError
        try:
            getattr(self.gd.grammar(data), self.gd.root_rule)() #call grammar(data).root_rule()
            return True
        except ParseError:
            return False

class PythonChecker(Checker):
    def __init__(self, module):
        Checker.__init__(self)
        self._matchFun = module["matchFun"]

    def check(self, data):
        return self._matchFun(data)


class PLYChecker(Checker):
    def __init__(self, gd):
        Checker.__init__(self)
        self.module = gd.module

    def check(self, data):
        if isinstance(data, Iterable):
            data = "".join([str(x) for x in data])
        from ply import yacc, lex
        lexer = lex.lex(self.module)
        parser = yacc.yacc(module = self.module)
        from pydsl.Exceptions import ParseError
        try:
            parser.parse(data, lexer = lexer)
        except ParseError:
            return False
        return True

class StringChecker(Checker):
    def __init__(self, gd):
        Checker.__init__(self)
        self.gd = gd

    def check(self, data):
        if isinstance(data, Iterable):
            data = "".join([str(x) for x in data])
        return self.gd == str(data)

class JsonSchemaChecker(Checker):
    def __init__(self, gd):
        Checker.__init__(self)
        self.gd = gd

    def check(self, data):
        from jsonschema import validate, ValidationError
        try:
            validate(data, self.gd)
        except ValidationError:
            return False
        return True

class ChoiceChecker(Checker):
    def __init__(self, gd):
        Checker.__init__(self)
        self.gd = gd
        self.checkerinstances = [checker_factory(x) for x in self.gd]

    def check(self, data):
        data = self._normalize_input(data)
        return any((x.check(data) for x in self.checkerinstances))

class SequenceChecker(Checker):
    def __init__(self, sequence):
        Checker.__init__(self)
        from pydsl.Grammar import Grammar
        for x in sequence:
            if not isinstance(x, Grammar):
                raise TypeError("Expected grammar, got %s" % (x.__class__.__name__,))
        self.sequence = sequence

    def check(self,data):
        if len(self.sequence) != len(data):
            return False
        data = self._normalize_input(data)
        return all(check(self.sequence[x], data[x]) for x in range(len(self.sequence)))


class OneOrMoreChecker(Checker):
    def __init__(self, element):
        Checker.__init__(self)
        self.element = element

    def check(self, data):
        return bool(data) and all(check(self.element.element, x) for x in data)

class ZeroOrMoreChecker(Checker):
    def __init__(self, element):
        Checker.__init__(self)
        self.element = element

    def check(self, data):
        return all(check(self.element.element, x) for x in data)
