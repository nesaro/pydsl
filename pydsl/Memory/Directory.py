#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file is part of pydsl.
#
#pydsl is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pydsl is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

""" Directory storage """

from pydsl.Config import GLOBALCONFIG
from pypository.Directory import DirStorage as BaseDirStorage
from pypository.utils import ImmutableDict


class DirStorage(BaseDirStorage):
    """A collection of elements stored inside a directory"""
    @property
    def allowed_extensions(self):
        return [x["extension"] for x in GLOBALCONFIG.formatlist]

    @staticmethod
    def summary_from_filename(filepath):
        entry = [x for x in GLOBALCONFIG.formatlist if filepath.endswith(x["extension"])][0]
        return ImmutableDict(entry["summary_from_file"](filepath))

    def load(self, name):
        result = self._searcher.search(name)
        if len(result) > 1:
            LOG.error("Found two or more matches, FIXME: processing the first, should raise exception")
        if not result:
            raise KeyError(self.__class__.__name__ + name)
        filepath = list(result)[0]["filepath"]
        entries = [x for x in GLOBALCONFIG.formatlist if filepath.endswith(x["extension"])]
        for entry in entries:
            try:
                return entry["load_from_file"](filepath)
            except ValueError:
                continue
        raise ValueError("Unable to open: %s" % name)

