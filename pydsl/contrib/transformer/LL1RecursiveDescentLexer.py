#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (c) 2008-2012 Nestor Arocha Rodriguez

"""LL(1) Recursive Descent Lexer
second recipe of the book "Language implementation patterns

grammar NestedNameList;
list : '[' elements ']' ; // match bracketed list
elements : element (',' element)* ; // match comma-separated list
element : NAME | list ; // element is name or nested list
NAME : ('a'..'z' |'A'..'Z' )+ ; // NAME is sequence of >=1 letter
"""

tokenlist = ["NAME", "COMMA", "LBRACK", "RBRACK","EOF_TYPE"]



def function(inputdic, inputgrammar, outputdic):
    def nextToken(tl):
        import re
        while tl:
            current = tl[0]
            if current == "/":
                comment(tl)
                continue
            elif current == " ":
                tl.pop(0)
                continue
            elif current == ",":
                tl.pop(0)
                return ("COMMA", current)
            elif current == "[":
                tl.pop(0)
                return ("LBRACK", current)
            elif current == "]":
                tl.pop(0)
                return ("RBRACK", current)
            elif re.match("[a-zA-Z]", current):
                return name(tl)
            else:
                raise Exception
        return ("EOF_TYPE", "")


    def name(tl):
        import re
        string = ""
        while tl and re.match("[a-zA-Z]", tl[0]):
            char = tl.pop(0)
            string += char
        return ("NAME", string)

    inputlist = [x for x in inputdic["input"]]
    result = []
    result.append(nextToken(inputlist))
    while result[-1][0] != "EOF_TYPE":
        result.append(nextToken(inputlist))
    return {"output":result}


iclass = "PythonTransformer"
inputdic = {"input":"cstring"}
outputdic = {"output":"cstring"}


