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
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)
from pydsl.Memory.Loader import load_checker

class Checker(object):
    """ Ensures information follows a rule, protocol or has a shape.
    Provides only check function, for complex operations, use Grammar"""
    def __init__(self):
        pass

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

    def check(self, word):
        """returns True if any match any regexp"""
        try:
            data = str(word)
        except UnicodeDecodeError:
            return False
        if not data:
            return False
        return bool(self.__regexp.match(data))


class BNFChecker(Checker):
    """Calls another program to perform checking. Args are always file names"""
    def __init__(self, bnf, parser = "auto"):
        Checker.__init__(self)
        parser = bnf.options.get("parser",parser)
        if parser == "descent" or parser == "auto" or parser == "default":
            from pydsl.Parser.RecursiveDescent import RecursiveDescentParser
            self.__parser = RecursiveDescentParser(bnf)
        elif parser == "weighted":
            from pydsl.Parser.Weighted import WeightedParser
            self.__parser = WeightedParser(bnf)
        else:
            LOG.error("Wrong parser name: " + parser)
            raise Exception

    def check(self, data):
        try:
            return len(self.__parser.get_trees(data)) > 0
        except IndexError:
            return False 

class PythonChecker(Checker):
    def __init__(self, module):
        Checker.__init__(self)
        self._matchFun = module["matchFun"]

    def check(self, data):
        try:
            return self._matchFun(data)
        except UnicodeDecodeError:
            return False


class MongoChecker(Checker):
    def __init__(self, dic):
        Checker.__init__(self)
        self.mongodic = dic

    def check(self, data):
        return self.__auxcheck(self.mongodic, data)

    def __auxcheck(self, specdict, data):
        """Recursive checker implementation"""
        for key, spec in specdict.items():
            value = data.get(key)
            if key == "$or" and len(specdict) == 1:
                return any([self.__auxcheck(x, data) for x in spec])
            elif isinstance(spec, dict) and len(spec) == 1:
                operator = list(spec.keys())[0]
                operand = list(spec.values())[0]
                if operator == "$type":
                    if not load_checker(operand).check(str(value)):
                        return False
                elif operator == "$or":
                    if not any([self.__auxcheck({key:x}, data) for x in operand]):
                        return False
                else: #unknown operator
                    return spec == value
            elif isinstance(spec, dict):
                if not self.__auxcheck(spec, value):
                    return False
            else:
                if spec != value: 
                    return False
        return True

class PLYChecker(Checker):
    def __init__(self, gd):
        Checker.__init__(self)
        self.module = gd.module

    def check(self, data):
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
        return self.gd.string == str(data)

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

class AlphabetListChecker(Checker):
    def __init__(self, gd):
        Checker.__init__(self)
        from pydsl.Alphabet.Definition import AlphabetListDefinition
        if not isinstance(gd, AlphabetListDefinition):
            raise TypeError
        self.gd = gd
        from pydsl.Memory.Loader import load_checker
        self.checkerinstances = [load_checker(x) for x in self.gd.grammarlist]

    def check(self, data):
        for element in data:
            if not any([x.check(element) for x in self.checkerinstances]):
                return False
        return True

class EncodingChecker(Checker):
    def __init__(self, gd):
        Checker.__init__(self)
        self.gd = gd

    def check(self,data):
        encoding = self.gd.encoding
        if isinstance(data, str):
            try:
                data.encode(encoding)
            except UnicodeEncodeError:
                return False
            return True
        if isinstance(data, bytes):
            try:
                data.decode(encoding)
            except UnicodeDecodeError:
                return False
            return True
        return False
