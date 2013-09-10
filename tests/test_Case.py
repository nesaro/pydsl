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

import unittest

class TestCase(unittest.TestCase):
    def test_main_case(self):
        input_data = "1+2"
        from pydsl.Alphabet.Definition import Encoding
        ascii_encoding = Encoding("ascii")
        from pydsl.Memory.Loader import lexer_factory
        ascii_lexer = lexer_factory(ascii_encoding)
        ascii_tokens = [x for x in ascii_lexer(input_data)]
        self.assertListEqual([str(x) for x in ascii_tokens], ['1', '+', '2'])

        def concept_translator_fun(inputtokens):
            from pydsl.Alphabet.Token import Token
            result = []
            for x in inputtokens:
                if x == Token("1"):
                    result.append("one")
                elif x == Token("2"):
                    result.append("two")
                elif x == Token("+"):
                    result.append("addition")
                else:
                    raise Exception(x.__class__.__name__)

            return result
        def to_number(number):
            if number == "one":
                return 1
            if number == "two":
                return 2
 
        from pydsl.Lexer import ConceptTranslator
        to_concepts = ConceptTranslator(concept_translator_fun)
        math_expression_concepts = to_concepts(ascii_tokens)
        self.assertListEqual(math_expression_concepts, ['one', 'addition', 'two'])
        grammar_def = [
                "S ::= E",
                "E ::= one addition two",
                "one := String,one",
                "two := String,two",
                "addition := String,addition",
                ]
        from pydsl.Memory.File.BNF import strlist_to_production_set
        production_set = strlist_to_production_set(grammar_def)
        from pydsl.Parser.RecursiveDescent import RecursiveDescentParser
        rdp = RecursiveDescentParser(production_set)
        parse_tree = rdp(math_expression_concepts)
        from pydsl.Grammar.Symbol import NonTerminalSymbol
        def parse_tree_walker(tree):
            if tree.production.leftside[0] == NonTerminalSymbol("S"):
                return parse_tree_walker(tree.childlist[0])
            if tree.production.leftside[0] == NonTerminalSymbol("E"):
                return to_number(tree.production.rightside[0].gd.string) + to_number(tree.production.rightside[2].gd.string)
            else:
                raise Exception
            
        result = parse_tree_walker(parse_tree[0])
        self.assertEqual(result, 3)
