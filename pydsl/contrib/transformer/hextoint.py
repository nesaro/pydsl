#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2013 Nestor Arocha

def function(inputdic, inputgt, outputgt):
    if not inputdic["input"]:
        return {}
    numberstr = inputdic["input"]
    decimalnumber = int(numberstr, 16)
    return {"output":str(decimalnumber)}


iclass = "PythonTransformer"
inputdic = {"input":"hex"}
outputdic = {"output":"integer"}
