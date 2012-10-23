#!/usr/bin/python
# -*- coding: utf-8 -*-

#copyright (c) 2008-2012 Néstor Arocha Rodríguez

"""Image file recognizer"""

def matchFun(input):
    content = input #FIXME: assuming bytes
    import imghdr
    return(bool(imghdr.what(None, content)))


iclass = "PythonGrammar"
