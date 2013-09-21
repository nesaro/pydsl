#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2013 Nestor Arocha

"""Test Binary calls"""

import unittest
import os

class TestBinaries(unittest.TestCase):
    """Tests Main Class"""
    def testCheck(self):
        self.assertEqual(os.system("bin/check.py"),512)
        self.assertEqual(os.system("bin/check.py integer -e 1"),0)

    def testGuess(self):
        self.assertEqual(os.system("bin/guess.py"),512)
        self.assertEqual(os.system("bin/guess.py -e 1234"),0)

    def testSearch(self):
        self.assertEqual(os.system("bin/manager.py list"),0)
