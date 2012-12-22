#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Nestor Arocha

"""Test Binary calls"""

import unittest
import os

class TestBinaries(unittest.TestCase):
    """Tests Main Class"""
    def testCheck(self):
        self.assertEqual(os.system("python3 bin/check.py"),512)
        self.assertEqual(os.system("python3 bin/check.py integer -e 1"),0)

    def testGuess(self):
        self.assertEqual(os.system("python3 bin/guess.py"),512)
        self.assertEqual(os.system("python3 bin/guess.py -e 1234"),0)

    def testTranslate(self):
        self.assertEqual(os.system("python3 bin/translate.py"),512)

    def testSearch(self):
        #self.assertEqual(os.system("python3 bin/search.py"),0)
        from subprocess import Popen,PIPE
        p = Popen(['python3', 'bin/search.py'], stdout=PIPE)
        p.communicate()
        self.assertEqual(p.returncode, 0)

    def testDiff(self):
        pass
