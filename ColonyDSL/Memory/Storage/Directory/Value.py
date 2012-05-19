#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Néstor Arocha Rodríguez

"""Value DirLibrary Module"""

import logging
LOG = logging.getLogger("DirLibrary.Value")


def load_information(filename, binary = True):
    if binary:
        with open(filename, 'rb') as f:
            return f.read()
    else:
        with open(filename, 'r') as f:
            return f.read()

