#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Néstor Arocha Rodríguez

"""Any string """

iclass="PythonGrammar"
def matchFun(inputstr):
    try:
        str(inputstr)
    except UnicodeDecodeError:
        return False
    return True

