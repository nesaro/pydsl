#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is part of pydsl.
#
# pydsl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# pydsl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from pydsl.grammar.definition import Grammar
from pydsl.check import checker_factory

__author__ = "Ptolom"
__copyright__ = "Copyright 2014, Ptolom"
__email__ = "ptolom@hexifact.co.uk"

class ParsleyGrammar(Grammar):
    def __init__(self, rules, root_rule="expr", repository=None):
        import parsley
        Grammar.__init__(self)
        repo=dict(repository or {})
        for key in repo:
            if isinstance(repo[key], Grammar):
                repo[key] = checker_factory(repo[key])
        self.grammar=parsley.makeGrammar(rules, repo)
        self.root_rule=root_rule 
