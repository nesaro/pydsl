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

"""loader class"""
from pydsl.Alphabet.Definition import Encoding

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

def load_checker(grammar):
    from pydsl.Grammar.BNF import BNFGrammar
    from pydsl.Grammar.Definition import PLYGrammar, RegularExpressionDefinition, MongoGrammar, StringGrammarDefinition, PythonGrammar
    from pydsl.Alphabet.Definition import AlphabetListDefinition
    if isinstance(grammar, str):
        grammar = load(grammar)
    if isinstance(grammar, BNFGrammar):
        from pydsl.Checker import BNFChecker
        return BNFChecker(grammar)
    elif isinstance(grammar, RegularExpressionDefinition):
        from pydsl.Checker import RegularExpressionChecker
        return RegularExpressionChecker(grammar)
    elif isinstance(grammar, PythonGrammar) or isinstance(grammar, dict) and "matchFun" in grammar:
        from pydsl.Checker import PythonChecker
        return PythonChecker(grammar)
    elif isinstance(grammar, MongoGrammar):
        from pydsl.Checker import MongoChecker
        return MongoChecker(grammar["spec"])
    elif isinstance(grammar, PLYGrammar):
        from pydsl.Checker import PLYChecker
        return PLYChecker(grammar)
    elif isinstance(grammar, AlphabetListDefinition):
        from pydsl.Checker import AlphabetListChecker
        return AlphabetListChecker(grammar)
    elif isinstance(grammar, StringGrammarDefinition):
        from pydsl.Checker import StringChecker
        return StringChecker(grammar)
    elif isinstance(grammar, Encoding):
        from pydsl.Checker import EncodingChecker
        return EncodingChecker(grammar)
    else:
        raise ValueError(grammar)

def load_lexer(alphabet):
    from pydsl.Alphabet.Definition import AlphabetListDefinition
    if isinstance(alphabet, str):
        alphabet = load(alphabet)
    if isinstance(alphabet, AlphabetListDefinition):
        from pydsl.Lexer import AlphabetListLexer
        return AlphabetListLexer(alphabet)
    elif isinstance(alphabet, Encoding):
        from pydsl.Lexer import EncodingTranslator
        return EncodingTranslator(alphabet)
    else:
        raise ValueError(alphabet)

def load_parser(grammar, parser = "auto"):
    if isinstance(grammar, str):
        grammar = load(grammar)
    from pydsl.Grammar.BNF import BNFGrammar
    if isinstance(grammar, BNFGrammar):
        if parser == "descent":
            from pydsl.Parser.RecursiveDescent import RecursiveDescentParser
            return RecursiveDescentParser(grammar)
        elif parser in ("auto" , "default" , "weighted"):
            #TODO Guess best parser
            from pydsl.Parser.Weighted import WeightedParser
            return WeightedParser(grammar)
        else:
            raise Exception("Wrong parser name: " + parser)
    else:
        raise ValueError(grammar)

def load_validator(grammar):
    if isinstance(grammar, str):
        grammar = load(grammar)
    from pydsl.Grammar.BNF import BNFGrammar
    if isinstance(grammar, BNFGrammar):
        from pydsl.Validate import BNFValidator
        return BNFValidator(grammar)
    else:
        raise ValueError(grammar)

def _load_checker(originaldic):
    """Converts {"channelname","type"} into {"channelname",instance}"""
    from pydsl.Memory.Loader import load_checker
    result = {}
    for key in originaldic:
        result[key] = load_checker(str(originaldic[key]))
    return result

def load_translator(function):
    if isinstance(function, str):
        function = load(function)
    from pydsl.Grammar.Definition import PLYGrammar
    if isinstance(function, PLYGrammar):
        from pydsl.Translator.Grammar import PLYTranslator
        return PLYTranslator(function)
    if isinstance(function, dict):
        from pydsl.Translator.Grammar import PythonTranslator
        function['inputdic'] = _load_checker(function['inputdic'])
        function['outputdic'] = _load_checker(function['outputdic'])
        return PythonTranslator(**function)
    from pyparsing import OneOrMore
    if isinstance(function, OneOrMore):
        from pydsl.Translator import PyParsingTranslator
        return PyParsingTranslator(function)
    raise ValueError(function)

def load(identifier, memorylist = None):
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    from pypository.Loader import load
    return load(identifier, memorylist)

def search(query, memorylist = None):
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    from pypository.Loader import search
    return search(query, memorylist)
