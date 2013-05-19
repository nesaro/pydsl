#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2013 Nestor Arocha

"""IntegerTreeGrammar language"""

#{<int>\0parent\0<int>;}

def matchFun(input):
    parentrelationlist = str(input).split(";")
    from pydsl.Memory.Loader import load
    integer = load("integer")
    for parentrelation in parentrelationlist:
        relation = parentrelation.split("\0")
        if len(relation) < 2:
            break
        if len(relation) != 3:
            return False
        if relation[1] != "parent":
            return False
        if not integer.check(relation[0]):
            return False
        if not integer.check(relation[2]):
            return False
    return True


iclass = "PythonGrammar"
auxdic =  {"int":"integer"}
