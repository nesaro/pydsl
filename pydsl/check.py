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
__copyright__ = "Copyright 2008-2017, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
from collections import Iterable
from jsonschema import FormatChecker
from pydsl.exceptions import ParseError, UnknownAlphabet
from pydsl.token import Token
LOG = logging.getLogger(__name__)


def check(definition, data, *args, **kwargs):
    """Checks if the input follows the definition"""
    checker = checker_factory(definition)
    return checker(data, *args, **kwargs)

def checker_factory(grammar):
    from pydsl.grammar.BNF import BNFGrammar
    from pydsl.grammar.PEG import Sequence, Choice, OneOrMore, ZeroOrMore
    from pydsl.grammar.definition import PLYGrammar, RegularExpression, String, PythonGrammar, JsonSchema
    from pydsl.grammar.parsley import ParsleyGrammar
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

    def __call__(self, *args, **kwargs):
        return self.check(*args, **kwargs)

    def check(self, value):# -> bool:
        raise NotImplementedError

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
            data = "".join(str(x) for x in data)
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
        parser = bnf.options.get("parser", parser)
        if parser in ("descent", "auto", "default", None):
            from pydsl.parser.backtracing import BacktracingErrorRecursiveDescentParser
            self.__parser = BacktracingErrorRecursiveDescentParser(bnf)
        else:
            raise ValueError("Unknown parser : " + parser)

    def check(self, data):
        if isinstance(data, str):
            from pydsl.token import PositionToken
            from pydsl.encoding import ascii_encoding
            data = [PositionToken(x, ascii_encoding, i, i+1) for i,x in enumerate(data)]
        if not isinstance(data, Iterable):
            raise TypeError(data)
        if not all(check(self.gd.alphabet, [x]) for x in data):
            print("CHECKING BNF FAILED {} {} data {}".format(self.gd, data, data))
            LOG.warning("Invalid input: %s,%s" % (self.gd.alphabet, data))
            return False
        print("CHECKING BNF 2 {} {}".format(self.gd, [x.content for x in data]))
        try:
            result = self.__parser.get_trees(data)
            print("TREES {}".format(result))
            print("TREES {}".format(len(result) > 0))
            return len(result) > 0
        except (IndexError, UnknownAlphabet):
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
        if isinstance(data, Iterable) and not isinstance(data, str):
            data = "".join([str(x) for x in data])
        if not isinstance(data, str):
            raise TypeError(data.__class__.__name__)
        return self.gd == str(data)

def formatchecker_factory(**checkerdict):
    """Converts a dictionary of strings:checkers into a formatchecker object"""
    fc = FormatChecker()
    for format_name, checker in checkerdict.items():
        fc.checks(format_name)(checker)
    return fc


class JsonSchemaChecker(Checker):
    def __init__(self, gd, formatdict = None):
        Checker.__init__(self)
        self.gd = gd
        formatdict = formatdict or {}
        self.formatchecker = formatchecker_factory(**formatdict)

    def check(self, data, raise_exceptions = False):
        from jsonschema import validate, ValidationError
        try:
            validate(data, self.gd, format_checker = self.formatchecker)
        except ValidationError:
            if raise_exceptions:
                raise
            return False
        return True

class ChoiceChecker(Checker):
    def __init__(self, gd):
        Checker.__init__(self)
        self.gd = gd
        self.checkerinstances = [checker_factory(x) for x in self.gd]

    def check(self, data):
        print("checking Choice {}, {}".format(self.gd, data))
        if not isinstance(data, Iterable):
            raise TypeError(data.__class__.__name__)
        return any((x.check(data) for x in self.checkerinstances))

class SequenceChecker(Checker):
    def __init__(self, sequence):
        Checker.__init__(self)
        from pydsl.grammar import Grammar
        for x in sequence:
            if not isinstance(x, Grammar):
                raise TypeError("Expected grammar, got %s" % (x.__class__.__name__,))
        self.sequence = sequence

    def check(self, data):
        if not isinstance(data, Iterable):
            raise TypeError(data.__class__.__name__)
        if len(self.sequence) != len(data):
            return False
        return all(check(self.sequence[x], [data[x]]) for x in range(len(self.sequence)))


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
