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

"""Python Transformers"""

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"

import logging
LOG = logging.getLogger(__name__)

class PythonTranslator(object):
    """ Python function based translator """
    def __init__(self, inputdic, outputdic, function):
        self._function = function
        self.inputchanneldic = inputdic
        self.outputchanneldic = outputdic

    def __call__(self, *args, **kwargs):
        for dickey in kwargs.keys():
            if not self.inputchanneldic[dickey].check(kwargs[dickey]):
                raise ValueError("Invalid value %s for input %s (%s)" % (kwargs[dickey], dickey, self))
        result = self._function(*args, **kwargs)
        return result

class PLYTranslator(object):
    def __init__(self, grammardefinition):
        self.module = grammardefinition.module

    def __call__(self, input):
        from ply import yacc, lex
        lexer = lex.lex(self.module)
        parser = yacc.yacc(debug=0, module = self.module)
        return parser.parse(input, lexer = lexer)

class PyParsingTranslator(object):
    def __init__(self, root_symbol):
        self.root_symbol = root_symbol

    def __call__(self, input):
        return self.root_symbol.parseString(input)
