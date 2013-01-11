#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (c) 2008-2013 Nestor Arocha Rodriguez

"""Memoizing parser

grammar NestedNameList;
stat: list EOF | assing EOF;
assing : list '=' list
list : '[' elements ']' ; // match bracketed list
elements : element (',' element)* ; // match comma-separated list
element : NAME '=' NAME | NAME | list ; // element is name or nested list
NAME : ('a'..'z' |'A'..'Z' )+ ; // NAME is sequence of >=1 letter
"""

#tokenlist = ["NAME", "COMMA", "LBRACK", "RBRACK","EOF_TYPE"]



from pydsl.Alphabet.Lexer import Lexer as _Lexer


class memoized:
    def __init__(self, name):
        self.name = name 

    def __call__(self, func):
        def wrap(instance):
            failed = False
            if instance.speculating() and instance.alreadyParserRule(self.name, instance.index):
                return
            previndex = instance.index
            try:
                func(instance)
            except Exception as e:
                failed = True
            finally:
                if instance.speculating():
                    result = -1
                    if not failed:
                        result = instance.index
                    instance.memoize[(self.name, previndex)] = result
        return wrap              


class _Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lookahead = []
        self.markers = []
        self.index = 0
        self.memoize = {}

    def alreadyParserRule(self, name, index):
        memo = self.memoize.get((name, index))
        if not memo:
            return False
        if memo== -1:
            raise Exception
        self.index = memo
        return True

    def LT(self, i):
        """gets element from input"""
        self.sync(i)
        return self.lookahead[self.index+i-1]

    def match(self, x):
        if self.LT(1)[0] == x:
            self.consume()
        else:
            raise Exception("Not matched")

    def sync(self, i):
        """Fills from index to index +i """
        if self.index + i > len(self.lookahead):
            n = self.index + i - len(self.lookahead)
            self.fill(n)


    def fill(self, n):
        """fills n elements"""
        for _ in range(n):
            self.lookahead.append(self.lexer.nextToken())

    def consume(self):
        self.index += 1
        if self.index == len(self.lookahead) and not self.speculating():
            self.index = 0
            self.lookahead = []
            self.memoize = {}
        self.sync(1)

    def mark(self):
        self.markers.append(self.index)
        return self.index

    def release(self):
        marker = self.markers.pop()
        self.index = marker

    def speculating(self):
        return len(self.markers) > 0

class _ListParser(_Parser):
    def stat(self):
        if self.speculate_stat_1():
            self.rlist()
            self.match("EOF_TYPE")
        elif self.speculate_stat_2():
            self.assign()
            self.match("EOF_TYPE")
        else:
            raise Exception("No alternative for stat")

    def speculate_stat_1(self):
        success = True
        self.mark()
        try:
            self.rlist()
            self.match("EOF_TYPE")
        except Exception as e:
            success = False
        self.release()
        return success

    def speculate_stat_2(self):
        success = True
        self.mark()
        try:
            self.assign()
            self.match("EOF_TYPE")
        except Exception as e:
            success = False
        self.release()
        return success

    def assign(self):
        self.rlist()
        self.match("EQUAL")
        self.rlist()


    @memoized("rlist")
    def rlist(self):
        self.match("LBRACK")
        self.elements()
        self.match("RBRACK")

    def elements(self):
        self.element()
        while self.LT(1)[0] == "COMMA":
            self.match("COMMA")
            self.element()

    def element(self):
        if self.LT(1)[0] == "NAME" and self.LT(2)[0] == "EQUAL":
            self.match("NAME")
            self.match("EQUAL")
            self.match("NAME")
        elif self.LT(1)[0] == "NAME":
            self.match("NAME")
        elif self.LT(1)[0] == "LBRACK":
            self.rlist()
        else: 
            raise Exception



class _ListLexer(_Lexer):
    def nextToken(self):
        import re
        from pydsl.Grammar.Lexer import finalchar
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
    result = b.stat()

    return {"output":result}


iclass = "PythonTransformer"
inputdic = {"input":"cstring"}
outputdic = {"output":"cstring"}


