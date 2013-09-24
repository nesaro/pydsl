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

import logging
LOG = logging.getLogger(__name__)
from pydsl.Memory.Loader import load
from pydsl.Parser.Parser import parser_factory


class Validator(object):
    """Receives a grammar and an input that doesn't belong to the grammar, 
    expands the grammar by parsing it, returns a list of what's needed 
    to become grammar compatible"""
    def __init__(self, grammar):
        self.gd = grammar

    def __call__(self, inputstring): #-> set
        raise NotImplementedError


class BNFValidator(Validator):
    def __call__(self, inputstring):
        parser = parser_factory(self.gd, "descent")
        resulttrees = parser.get_trees(inputstring, True)
        return resulttrees


def validator_factory(grammar):
    if isinstance(grammar, str):
        grammar = load(grammar)
    from pydsl.Grammar.BNF import BNFGrammar
    if isinstance(grammar, BNFGrammar):
        return BNFValidator(grammar)
    else:
        raise ValueError(grammar)


def validate(definition, data):
    return validator_factory(definition)(data)