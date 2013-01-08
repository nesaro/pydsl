#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Grammar 2 Recursive Descent Parser Recognizer
First recipe of the book "Language implementation patterns

grammar NestedNameList;
list : '[' elements ']' ; // match bracketed list
elements : element (',' element)* ; // match comma-separated list
element : NAME | list ; // element is name or nested list
NAME : ('a'..'z' |'A'..'Z' )+ ; // NAME is sequence of >=1 letter
"""


def matchFun(inputstr):
    def look_ahead(tl):
        if tl[0] == "[":
            return "list"
        elif tl[0] == ",":
            return ","

    def mlist(tl):
        if tl.pop(0) != "[":
            return False
        if not elements(tl):
            return False
        if tl.pop(0) != "]":
            return False
        return True

    def elements(tl):
        if not element(tl):
            return False
        while(look_ahead(tl) == ","):
            tl.pop(0)
            if not element(tl):
                return False
        return True

    def element(tl):
        if look_ahead(tl) == "list":
            if not mlist(tl):
                return False
        else:
            if not name(tl):
                return False
        return True

    def name(tl):
        import re
        if not re.match("[a-zA-Z]", tl.pop(0)):
            return False
        while tl and re.match("[a-zA-Z]", tl[0]):
            tl.pop(0)
        return True

    inputlist = [x for x in inputstr]
    return element(inputlist) and not len(inputlist)


iclass = "PythonGrammar"


