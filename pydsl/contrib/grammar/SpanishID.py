#!/usr/bin/python
# -*- coding: utf-8 -*-

#copyright (c) 2008-2013 Nestor Arocha

"""spanish id number grammar"""

def matchFun(inputstr):
    dni = str(inputstr)
    if len(dni) != 9:
        return False
    string = 'TRWAGMYFPDXBNJZSQVHLCKE'
    resto = int(dni[:8]) % 23
    if dni[-1].lower() == string[resto].lower():
        return True
    return False

def propFun(inputstr, propertyname):
    dni = inputstr
    if propertyname == "number":
        return dni[:8]
    elif propertyname == "letter":
        return dni[:-1]
    else:
        return False

iclass = "PythonGrammar"

