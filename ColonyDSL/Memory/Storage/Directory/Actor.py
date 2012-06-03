#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2012 Néstor Arocha Rodríguez

from .DirStorage import DirStorage
import logging
LOG = logging.getLogger("DirStorage.Actor")

class ActorFileStorage(DirStorage):
    def __init__(self, path):
        DirStorage.__init__(self, path, [".py"])

    def provided_iclasses(self) -> list:
        return ["Actor"]
