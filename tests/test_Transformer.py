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

def recursivecall(input, auxt ,inputgrammars, outputgrammars):
    """Ignores input"""
    return {"output":auxt["myadder"]({"input":"1+e"})}

def integerextractor(input, inputgrammars, outputgrammars):
    return {"output":inputgrammars["input"].get_groups(input["input"],"Operator")[0]}

def ope1(childlist):
    """&& True"""
    return childlist[1]

def ope2(childlist):
    el0, el1 = childlist
    if el0 != 'True' or el1 != 'True':
        return 'False'
    return 'True'


def opefinal(vardict):
    return str(vardict.getInitialSymbol())

class TestTransformer(unittest.TestCase):
    """Tests Transformers"""
    def setUp(self):
        from pydsl.Function.Python import PythonTransformer
        from pydsl.Function.ExternalProgram import ExternalProgramFunction 
        self.__gt1 = PythonTransformer({"input":"integerop"},{"output":"cstring"},integerextractor)
        self.__text = ExternalProgramFunction({"input":"cstring"},{"output":"cstring"}, ["echo","#{input}"])

    def testProperty(self):
        """Tests an extractor Transformer"""
        result = self.__gt1({"input":"1+1"})
        assert(str(result["output"]) == "+")

    def testExternal(self):
        result = self.__text({"input":"1+1"})
        self.assertEqual(str(result["output"]),"1+1\n")

class TestHostTransformer(unittest.TestCase):
    """Test recursive transformer"""
    def setUp(self):
        from pydsl.Function.Python import HostPythonTransformer
        self.__gt1 = HostPythonTransformer({"input":"cstring"},{"output":"cstring"},{"myadder":"simple-adder"},recursivecall)

    def testError(self):
        self.assertRaises(ValueError,self.__gt1, {"input":"1"})

class TestSyntaxDirectedTransformer(unittest.TestCase):
    def setUp(self):
        from pydsl.Function.SyntaxDirected import SyntaxDirectedTransformer
        self.__gt1 = SyntaxDirectedTransformer("LogicalExpression", "cstring",
                {"OperatorExpression::=<TS: grammarTrueFalse> <NonTS: RestExpression>":ope1,
                    'Expression::=<NonTS: OperatorExpression>':ope2})

    def testCall(self):
        self.assertTrue(self.__gt1("True&&True"))

    def testError(self):
        pass

