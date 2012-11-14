#!/usr/bin/python
# -*- coding: utf-8 -*-

#copyright (c) 2008-2011 Néstor Arocha Rodríguez

"""Protocols"""

def matchFun(inputd):
    inputs = str(inputd)
    return inputs.find("://") != -1

def propFun(inputd, propertyname):
    inputs = str(inputd)
    protocol, rest = inputs.split("://")
    if propertyname == "protocol":
        return protocol
    if "?" in rest:
        path, options = rest.split("?")
        if propertyname == "path":
            return path
        elif propertyname == "options":
            return options
    else:
        if propertyname == "path":
            return rest

iclass = "PythonGrammar"


