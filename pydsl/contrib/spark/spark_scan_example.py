#  Copyright (c) 1999-2000 John Aycock
#  
#  Permission is hereby granted, free of charge, to any person obtaining
#  a copy of this software and associated documentation files (the
#  "Software"), to deal in the Software without restriction, including
#  without limitation the rights to use, copy, modify, merge, publish,
#  distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to
#  the following conditions:
#  
#  The above copyright notice and this permission notice shall be
#  included in all copies or substantial portions of the Software.
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#
#  Why would I write my own when GvR maintains this one?
#
import tokenize

class Token:
    def __init__(self, type, attr=None, lineno='???'):
        self.type = type
        self.attr = attr
        self.lineno = lineno

    def __cmp__(self, o):
        return cmp(self.type, o)
    ###
    def __repr__(self):
        return str(self.type)

_map = {
    tokenize.ENDMARKER    : 'ENDMARKER',
    tokenize.NAME         : 'NAME',
    tokenize.NUMBER        : 'NUMBER',
    tokenize.STRING        : 'STRING',
    tokenize.NEWLINE    : 'NEWLINE',
    tokenize.INDENT        : 'INDENT',
    tokenize.DEDENT        : 'DEDENT',
}

_rw = {
    'and'        : None,
    'assert'    : None,
    'break'        : None,
    'class'        : None,
    'continue'    : None,
    'def'        : None,
    'del'        : None,
    'elif'        : None,
    'else'        : None,
    'except'    : None,
    'exec'        : None,
    'finally'    : None,
    'for'        : None,
    'from'        : None,
    'global'    : None,
    'if'        : None,
    'import'    : None,
    'in'        : None,
    'is'        : None,
    'lambda'    : None,
    'not'        : None,
    'or'        : None,
    'pass'        : None,
    'print'        : None,
    'raise'        : None,
    'return'    : None,
    'try'        : None,
    'while'        : None,
}

def scan(f):
    tokens = []

    def callback(value, lexeme, lineno_column, end, line, list=tokens):
        attr = None
        type = lexeme
        lineno, column = lineno_column
        if value in (tokenize.COMMENT, tokenize.NL):
            return
        elif value in _map:
            if value != tokenize.NAME or not _rw.has_key(lexeme):
                attr = lexeme
                type = _map[value]

        t = Token(type, attr=attr, lineno=lineno)
        list.append(t)

    tokenize.tokenize(f.readline, callback)
    return tokens
