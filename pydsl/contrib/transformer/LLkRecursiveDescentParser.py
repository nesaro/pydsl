#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (c) 2008-2013 Nestor Arocha Rodriguez

"""LL(1) Recursive Descent Lexer
second recipe of the book "Language implementation patterns

grammar NestedNameList;
list : '[' elements ']' ; // match bracketed list
elements : element (',' element)* ; // match comma-separated list
element : NAME | list ; // element is name or nested list
NAME : ('a'..'z' |'A'..'Z' )+ ; // NAME is sequence of >=1 letter
"""

#tokenlist = ["NAME", "COMMA", "LBRACK", "RBRACK","EOF_TYPE"]

from pydsl.Alphabet.Lexer import Lexer as _Lexer

class _Parser:
    def __init__(self, lexer, size = 3):
        self.lexer = lexer
        self.currenttoken = None
        self.lookahead = []
        self.size = size
        for _ in range(size):
            self.consume()

    def match(self, x):
        if self.lookahead[0][0] == x:
            self.consume()
        else:
            raise Exception

    def consume(self):
        self.lookahead.append(self.lexer.nextToken())
        if len(self.lookahead) > 3:
            self.lookahead.pop(0)

class _ListParser(_Parser):
    def rlist(self):
        self.match("LBRACK")
        self.elements()
        self.match("RBRACK")

    def elements(self):
        self.element()
        while self.lookahead[0][0] == "COMMA":
            self.match("COMMA")
            self.element()

    def element(self):
        if self.lookahead[0][0] == "NAME" and self.lookahead[1][0] == "EQUAL":
            self.match("NAME")
            self.match("EQUAL")
            self.match("NAME")
        elif self.lookahead[0][0] == "NAME":
            self.match("NAME")
        elif self.lookahead[0][0] == "LBRACK":
            self.rlist()
        else: 
            raise Exception



class _ListLexer(_Lexer):
    def nextToken(self):
        import re
        from pydsl.Alphabet.Lexer import finalchar
        while self.current != finalchar:
            if self.current == "/":
                self.comment(tl)
                continue
            elif self.current == " ":
                self.consume()
                continue
            elif self.current == ",":
                return self.comma()
            elif self.current == "[":
                return self.lbrack()
            elif self.current == "]":
                return self.rbrack()
            elif self.current == "=":
                return self.equals()
            elif re.match("[a-zA-Z]", self.current):
                return self.name()
            else:
                raise Exception
        return "EOF_TYPE", ""

    def comma(self):
        current = self.current
        self.match(",")
        return "COMMA", current

    def equals(self):
        current = self.current
        self.match("=")
        return "EQUAL", current

    def lbrack(self):
        current = self.current
        self.match("[")
        return "LBRACK", current

    def rbrack(self):
        current = self.current
        self.match("]")
        return "RBRACK", current

    def name(self):
        import re
        string = ""
        from pydsl.Grammar.Lexer import finalchar
        while self.current != finalchar and re.match("[a-zA-Z]", self.current):
            string += self.current
            self.consume()
        return "NAME", string


def function(inputdic, inputgrammar, outputdic):
    a = _ListLexer(inputdic["input"])
    b = _ListParser(a)
    result = b.rlist()

    return {"output":result}


iclass = "PythonTransformer"
inputdic = {"input":"cstring"}
outputdic = {"output":"cstring"}


