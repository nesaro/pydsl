#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2013 Nestor Arocha

def function(inputdic, inputgt, outputgt):
    filename = inputdic["input"].string
    with open(filename, 'r') as f:
        result = f.read()
        result = str(result)
        return {"output":result}


iclass = "PythonTransformer"
inputdic = {"input":"unixPathGrammar"}
outputdic = {"output":"Hex"}
