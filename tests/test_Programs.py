#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Nestor Arocha 

import unittest

def maketestFromGT(gtname, inputexpression, outputdic):
    """Makes a test and returns True if it finishes successfully"""
    values = {}
    values["expression"] = inputexpression
    values["directreturn"] = True
    values["outputfiledic"] = None    
    values["inputfiledic"] = None
    values["pipemode"] = None    
    from pydsl.Memory.Loader import load
    gt = load(gtname)
    result = gt(inputexpression)
    for key in outputdic.keys():
        if result[key] != outputdic[key]:
            return False
    return True

class TestProgramsLibrary(unittest.TestCase):
    """Tests Main Class"""
    def setUp(self):
        pass

    def testRoman(self):
        self.assertTrue(maketestFromGT("simple-adder-roman", {"input":"1+2"}, {"output":"III"}))

    def testIntegerDivisor(self):
        self.assertTrue(maketestFromGT("integerDivisor", {'input':'123'}, {"output":'123\x00parent\x003;123\x00parent\x0041;'}))

    def testIntegerDivisibilityTree(self):
        self.assertTrue(maketestFromGT("integerToDivisibilityTree", {'input':'8'}, {"output":'8\x00parent\x002;8\x00parent\x004;4\x00parent\x002;'}))

    def testAdder(self):
        self.assertTrue(maketestFromGT("simple-adder", {'input':'1+2'}, {"output":"3"}))

    def testTokenAdder(self):
        self.assertTrue(maketestFromGT("simple-adder", {'input':"11+1"}, {"output":"12"}))
        self.assertRaises(ValueError, maketestFromGT ,"simple-adder", {"input":"EE"}, {'source':"['separator', 'simple-adder']", 'error':'Grammar'})

    def testTokenBoardTransformer(self):
        self.assertTrue(maketestFromGT("board-adder-roman", {"input":"1+2"}, {"output":"III"}))

    def testHostPythonGT(self):
        self.assertTrue(maketestFromGT("integerToDivisibilityTree", {"input":"24"}, {"output":'24\x00parent\x002;24\x00parent\x003;24\x00parent\x004;24\x00parent\x006;24\x00parent\x008;24\x00parent\x0012;4\x00parent\x002;6\x00parent\x002;6\x00parent\x003;8\x00parent\x002;8\x00parent\x004;12\x00parent\x002;12\x00parent\x003;12\x00parent\x004;12\x00parent\x006;4\x00parent\x002;4\x00parent\x002;6\x00parent\x002;6\x00parent\x003;'}))


