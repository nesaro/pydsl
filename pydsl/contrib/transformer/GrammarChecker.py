#!/usr/bin/python
# -*- coding: utf-8 -*-

def function(inputdic, inputgt, outputgt):
    grammarname =  str(inputdic['grammar'])
    from pydsl.Memory.Loader import load_checker
    grammar = load_checker(grammarname)
    result = grammar.check(inputdic['string'])
    return {"output":str(result)}


inputdic = {"grammar":"cstring", "string":"cstring"}
outputdic = {"output":"TrueFalse"}
iclass = "PythonTransformer"
