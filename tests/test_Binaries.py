#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Néstor Arocha Rodríguez

"""Test Binary calls"""

import unittest

class TestBinaries(unittest.TestCase):
    """Tests Main Class"""
    def setUp(self):
        pass

    def testCheck(self):
        import os
        self.assertEqual(os.system("python3 bin/check.py"),512)
        self.assertEqual(os.system("python3 bin/check.py integer -e 1"),0)

    def testGuess(self):
        import os
        self.assertEqual(os.system("python3 bin/guess.py"),512)
        self.assertEqual(os.system("python3 bin/guess.py -e 1234"),0)

    def testTranslate(self):
        import os
        self.assertEqual(os.system("python3 bin/translate.py"),512)


    def testConvert(self):
        import os
        self.assertEqual(os.system("python3 bin/convert.py"),512)

    def testSearch(self):
        import os
        self.assertEqual(os.system("python3 bin/search.py"),512)

