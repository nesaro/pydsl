#!/usr/bin/python
# -*- coding: utf-8 -*-

def function(inputdic, inputgt, outputgt):
    output = ""
    value1 = str(inputdic["int1"])
    value2 = str(inputdic["int2"])
    if value1 != "" and value2 != "": 
        output = str(int(value1) + int(value2))
    return {"int":output}

inputdic = {"int1":"integer", "int2":"integer"}
outputdic = {"int":"integer"}
iclass = "PythonTransformer"
