#!/usr/bin/python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright 2008-2013, Nestor Arocha"

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

    def testAdder(self):
        self.assertTrue(maketestFromGT("simple-adder", {'input':'1+2'}, {"output":"3"}))

    def testTokenAdder(self):
        self.assertTrue(maketestFromGT("simple-adder", {'input':"11+1"}, {"output":"12"}))
        self.assertRaises(ValueError, maketestFromGT ,"simple-adder", {"input":"EE"}, {'source':"['separator', 'simple-adder']", 'error':'Grammar'})

    def testTokenBoardTransformer(self):
        self.assertTrue(maketestFromGT("board-adder-roman", {"input":"1+2"}, {"output":"III"}))
