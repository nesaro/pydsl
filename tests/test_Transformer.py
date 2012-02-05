#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of ColonyDSL.
#
#ColonyDSL is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#ColonyDSL is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with ColonyDSL.  If not, see <http://www.gnu.org/licenses/>.


__author__ = "Néstor Arocha Rodríguez"
__copyright__ = "Copyright 2008-2012, Néstor Arocha Rodríguez"
__email__ = "nesaro@gmail.com"


import unittest

def recursivecall(input, auxt ,inputgrammars, outputgrammars, evfunctions):
    """Ignora la entrada"""
    return {"output":auxt["myadder"].call({"input":"1+e"})}

def integerextractor(input, inputgrammars, outputgrammars, evfunctions):
    return {"output":inputgrammars["input"].get_groups(input["input"],"Operator")[0]}

def opidentifier(vardict, rulename, dpr):
    vardict.setByNameAndBorders(rulename, dpr, {"VAL":dpr.tokenlist.string})

def ope1(vardict, rulename, dpr):
    vardict.setByNameAndBorders(rulename, dpr, {"1":"HI"})

def opefinal(vardict):
    return str(vardict.getInitialSymbol())

class TestTransformer(unittest.TestCase):
    """Tests Transformers"""
    def setUp(self):
        from ColonyDSL.Function.Transformer.Python import PythonTransformer
        from ColonyDSL.Function.Transformer.ExternalProgram import ExternalProgramTransformer
        self.__gt1 = PythonTransformer("test",{"input":"integerop"},{"output":"cstring"},integerextractor)
        self.__text = ExternalProgramTransformer("test",{"input":"cstring"},{"output":"cstring"}, ["echo","#{input}"])

    def testProperty(self):
        result = self.__gt1.call({"input":"1+1"})
        assert(str(result["output"]) == "+")

    def testExternal(self):
        result = self.__text.call({"input":"1+1"})
        assert(str(result["output"]) == "1+1\n")

class TestHostTransformer(unittest.TestCase):
    """Test recursive transformer"""
    def setUp(self):
        from ColonyDSL.Function.Transformer.Python import HostPythonTransformer
        self.__gt1 = HostPythonTransformer("test",{"input":"cstring"},{"output":"cstring"},{"myadder":"simple-adder"},recursivecall)

    def testError(self):
        result = self.__gt1.call({"input":"1"})
        assert(str(result.bt[0]) == 'separator' and str(result.bt[1]) == "myadder" and str(result.bt[2]) == "test")


class TestSyntaxDirectedTransformer(unittest.TestCase):
    def setUp(self):
        from ColonyDSL.Function.Transformer.SyntaxDirected import SyntaxDirectedTransformer
        self.__gt1 = SyntaxDirectedTransformer("test",{"input":"LogicalExpression"},{"output":"cstring"}, {"OperatorExpression1":ope1, "Expression0":ope1 , "S0":ope1, "Expression2":ope1, "RestExpression0":ope1, "finally":opefinal})

    def testError(self):
        pass

