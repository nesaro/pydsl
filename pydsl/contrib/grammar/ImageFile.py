#!/usr/bin/python
# -*- coding: utf-8 -*-

#copyright (c) 2008-2013 Nestor Arocha

"""Image file recognizer"""

def matchFun(input):
    content = input #assuming bytes
    import imghdr
    try:
        return bool(imghdr.what(None, content))
    except:
        return False


iclass = "PythonGrammar"
