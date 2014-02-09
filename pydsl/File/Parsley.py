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


from pydsl.Grammar.Parsley import ParsleyGrammar

__author__ = "Ptolom"
__copyright__ = "Copyright 2014, Ptolom"
__email__ = "ptolom@hexifact.co.uk"

#!/usr/bin/python
def load_parsley_grammar_file(filepath, root_rule, repository={}):
    with open(filepath,'r') as file:
        return ParsleyGrammar(file.read(), root_rule, repository)




