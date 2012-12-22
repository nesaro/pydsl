#!/usr/bin/python
# -*- coding: utf-8 -*-

#copyright (c) 2008-2012 Nestor Arocha

"""Image file recognizer"""

def matchFun(input):
    content = input #assuming bytes
    import imghdr
    return(bool(imghdr.what(None, content)))


iclass = "PythonGrammar"
