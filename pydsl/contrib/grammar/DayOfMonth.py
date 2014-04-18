#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2014 Nestor Arocha



def matchFun(myinput):
    from collections import Iterable
    if isinstance(myinput, Iterable):
        myinput = "".join([str(x) for x in myinput])
    strnumber = str(myinput)
    try:
        number = int(strnumber)
    except ValueError:
        return False
    if 0 < number < 32:
        return True
    return False

iclass = "PythonGrammar"
