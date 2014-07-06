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

import unittest
from pydsl.Encoding import ascii_encoding
from pydsl.Lex import lexer_factory
from pydsl.Parser.LL import LL1RecursiveDescentParser

class TestCase(unittest.TestCase):
    def test_main_case(self):
        input_data = "1+2"
        ascii_lexer = lexer_factory(ascii_encoding)
        ascii_tokens = [x.content for x in ascii_lexer(input_data)]
        self.assertListEqual([str(x) for x in ascii_tokens], ['1', '+', '2'])

        def concept_translator_fun(inputtokens):
            result = []
            for x in inputtokens:
                if x == "1":
                    result.append("one")
                elif x == "2":
                    result.append("two")
                elif x == "+":
                    result.append("addition")
                else:
                    raise Exception(x.__class__.__name__)

            return result
        def to_number(number):
            if number == [x for x in "one"]:
                return 1
            if number == [x for x in "two"]:
                return 2
 
        math_expression_concepts = concept_translator_fun(ascii_tokens)
        self.assertListEqual(math_expression_concepts, ['one', 'addition', 'two'])
        grammar_def = [
                "S ::= E",
                "E ::= one addition two",
                "one := String,one",
                "two := String,two",
                "addition := String,addition",
                ]
        from pydsl.File.BNF import strlist_to_production_set
        production_set = strlist_to_production_set(grammar_def, {})
        from pydsl.Parser.Backtracing import BacktracingErrorRecursiveDescentParser
        rdp = BacktracingErrorRecursiveDescentParser(production_set)
        parse_tree = rdp(math_expression_concepts)
        from pydsl.Grammar.Symbol import NonTerminalSymbol
        def parse_tree_walker(tree):
            if tree.symbol == NonTerminalSymbol("S"):
                return parse_tree_walker(tree.childlist[0])
            if tree.symbol == NonTerminalSymbol("E"):
                return to_number(tree.childlist[0].symbol.gd) + to_number(tree.childlist[2].symbol.gd)
            raise Exception
            
        result = parse_tree_walker(parse_tree[0])
        self.assertEqual(result, 3)


    def test_calculator_simple(self):
        grammar_def = [
                "S ::= E",
                "E ::= number operator number",
                "number := Word,integer,max",
                "operator := String,+",
                ]
        from pydsl.File.BNF import strlist_to_production_set
        from pydsl.Grammar import RegularExpression
        repository = {'integer':RegularExpression("^[0123456789]*$")}
        production_set = strlist_to_production_set(grammar_def, repository)
        rdp = LL1RecursiveDescentParser(production_set)
        parse_tree = rdp("1+2")

        def parse_tree_walker(tree):
            from pydsl.Grammar.Symbol import NonTerminalSymbol
            if tree.symbol == NonTerminalSymbol("S"):
                return parse_tree_walker(tree.childlist[0])
            if tree.symbol == NonTerminalSymbol("E"):
                return int(str(tree.childlist[0].content)) + int(str(tree.childlist[2].content))
            else:
                raise Exception
            
        result = parse_tree_walker(parse_tree[0])
        self.assertEqual(result, 3)
        from pydsl.Grammar.PEG import Choice
        from pydsl.Grammar.Definition import String, RegularExpression
        from pydsl.Encoding import ascii_encoding
        math_alphabet = Choice([RegularExpression("^[0123456789]*$"),Choice([String('+')])])
        from pydsl.Lex import lex
        tokens = [x[0] for x in lex(math_alphabet, ascii_encoding, "11+2")]
        parse_tree = rdp(tokens)
        result = parse_tree_walker(parse_tree[0])
        self.assertEqual(result, 13)

