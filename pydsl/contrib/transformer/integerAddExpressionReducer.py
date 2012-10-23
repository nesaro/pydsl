#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Nestor Arocha Rodríguez

def function(inputdic, inputgt, outputgt):
    inputData = inputdic["input"]
    if inputData:  
        integerlist = inputData.split("+")
        if len(integerlist) == 2:
            output1 = integerlist[0]
            output2 = integerlist[1]
        else:
            output1 = ""
            output2 = ""
        return {"int1":output1, "int2":output2}

inputdic = {"input":"integerop"}
outputdic = {"int1":"integer","int2":"integer"}
iclass = "PythonTransformer"

