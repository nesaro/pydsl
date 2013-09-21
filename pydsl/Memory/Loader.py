#!/usr/bin/python
# -*- coding: utf-8 -*-
# this file is part of pydsl.
#
# pydsl is free software: you can redistribute it and/or modify
# it under the terms of the gnu general public license as published by
# the free software foundation, either version 3 of the license, or
#(at your option) any later version.
#
# pydsl is distributed in the hope that it will be useful,
# but without any warranty; without even the implied warranty of
# merchantability or fitness for a particular purpose.  see the
# gnu general public license for more details.
#
# you should have received a copy of the gnu general public license
# along with pydsl.  if not, see <http://www.gnu.org/licenses/>.

"""loader class"""

__author__ = "nestor arocha"
__copyright__ = "copyright 2008-2013, nestor arocha"
__email__ = "nesaro@gmail.com"


def load(identifier, memorylist = None):
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    from pypository.Loader import load
    return load(identifier, memorylist)

def search(query, memorylist = None):
    if not memorylist:
        from pydsl.Config import GLOBALCONFIG
        memorylist = GLOBALCONFIG.memorylist
    from pypository.Loader import search
    return search(query, memorylist)
