#!/usr/bin/python
# -*- coding: utf-8 -*-

def function(inputdic, inputgt, outputgt):
    strfloat =  inputdic['input']
    realfloat = float(strfloat)
    realint = int(realfloat)
    return {"output":str(realint)}


inputdic = { "input":"float"}
outputdic = {"output":"integer"}
iclass = "PythonTransformer"
