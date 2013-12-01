#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of pydsl.
#
# pydsl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# pydsl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pydsl.  If not, see <http://www.gnu.org/licenses/>.

from pydsl.Grammar.Alphabet import Encoding
from pypository.utils import ImmutableDict
from pypository.List import ListStorage
from pypository.Memory import Memory

__author__ = "Nestor Arocha"
__copyright__ = "Copyright 2008-2013, Nestor Arocha"
__email__ = "nesaro@gmail.com"


class EncodingStorage(ListStorage):

    @staticmethod
    def _generatekey(element):
        return element

    @staticmethod
    def load(index):
        return Encoding(index)

    def generate_all_summaries(self):
        return tuple([ImmutableDict({"identifier": x, "value": x, "iclass": "Encoding"}) for x in self._content])


class RegexpDictStorage(Memory):
    def __init__(self, dictionary):
        Memory.__init__(self)
        self._content = dictionary

    def generate_all_summaries(self):# -> list:
        result = []
        from pypository.utils import ImmutableDict
        for key in self._content:
            result.append(ImmutableDict({"identifier":key, "regexp":self._content[key]["regexp"], "iclass":"RegularExpression"}))
        return result

    def load(self, index, **kwargs):
        import re
        flags = 0
        if "flags" in self._content[index]:
            if "i" in self._content[index]["flags"]:
                flags |= re.I
        from pydsl.Grammar.Definition import RegularExpression
        return RegularExpression(self._content[index]["regexp"], flags)

    def __iter__(self):
        self.index = 0
        self.cache = []
        self.cache += self.generate_all_summaries()
        return self

    def next(self):
        try:
            result = self.cache[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    def __contains__(self, index):
        return index in self._content