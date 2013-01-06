#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2013 Nestor Arocha

def matchFun(myinput):
    strnumber = str(myinput)
    try:
        number = int(strnumber)
    except ValueError:
        return False
    if number > 0 and number < 32:
        return True
    return False

iclass = "PythonGrammar"
