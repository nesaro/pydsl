#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2013 Nestor Arocha


def propFun(input, property):
    if property == "Operator":
        return input[1]

def matchFun(myinput, auxgrammardict):
    myinput = str(myinput)
    validoperators = ["+", "-", "*", "/"]
    operatorexists = False
    currentoperator = None
    for operator in validoperators:
        if operator in myinput:
            operatorexists = True
            currentoperator = operator
            break
    if not operatorexists:
        return False
    parts = myinput.split(currentoperator)
    if len(parts) != 2:
        return False
    for part in parts:
        if not auxgrammardict["integer"].check(part):
            return False
    return True

auxdic = {"integer":"integer"}
iclass = "PythonGrammar"
